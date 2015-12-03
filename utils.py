from uuid import uuid4
import os

import csv
import StringIO
from django.contrib.admin.utils import NestedObjects, quote
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils.text import capfirst
from django.utils.encoding import force_unicode


def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(path, filename)


def random_path_and_rename(path):
    return wrapper


class UnicodeWriter(object):
    """
    Like UnicodeDictWriter, but takes lists rather than dictionaries.

    Usage example:

    fp = open('my-file.csv', 'wb')
    writer = UnicodeWriter(fp)
    writer.writerows([
        [u'Bob', 22, 7],
        [u'Sue', 28, 6],
        [u'Ben', 31, 8],
        # \xc3\x80 is LATIN CAPITAL LETTER A WITH MACRON
        ['\xc4\x80dam'.decode('utf8'), 11, 4],
    ])
    fp.close()
    """
    def __init__(self, f, dialect=csv.excel_tab, encoding="utf-16", **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoding = encoding

    def writerow(self, row):
        # Modified from original: now using unicode(s) to deal with e.g. ints
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = data.encode(self.encoding)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class UnicodeDictWriter(UnicodeWriter):
    """
    A CSV writer that produces Excel-compatibly CSV files from unicode data.
    Uses UTF-16 and tabs as delimeters - it turns out this is the only way to
    get unicode data in to Excel using CSV.

    Usage example:

    fp = open('my-file.csv', 'wb')
    writer = UnicodeDictWriter(fp, ['name', 'age', 'shoesize'])
    writer.writerows([
        {'name': u'Bob', 'age': 22, 'shoesize': 7},
        {'name': u'Sue', 'age': 28, 'shoesize': 6},
        {'name': u'Ben', 'age': 31, 'shoesize': 8},
        # \xc3\x80 is LATIN CAPITAL LETTER A WITH MACRON
        {'name': '\xc4\x80dam'.decode('utf8'), 'age': 11, 'shoesize': 4},
    ])
    fp.close()

    Initially derived from http://docs.python.org/lib/csv-examples.html
    """

    def __init__(self, f, fields, dialect=csv.excel_tab,
                 encoding="utf-16", **kwds):
        super(UnicodeDictWriter, self).__init__(f, dialect, encoding, **kwds)
        self.fields = fields

    def writerow(self, drow):
        row = [drow.get(field, '') for field in self.fields]
        super(UnicodeDictWriter, self).writerow(row)


def get_merged_objects(objs, opts, user, admin_site, using):
    """
    Find all objects related to ``objs`` that should also be merged. ``objs``
    must be a homogenous iterable of objects (e.g. a QuerySet).

    Returns a nested list of strings suitable for display in the
    template with the ``unordered_list`` filter.

    """
    collector = NestedObjects(using=using)
    collector.collect(objs)
    perms_needed = set()

    def format_callback(obj):
        has_admin = obj.__class__ in admin_site._registry
        opts = obj._meta

        if has_admin:
            admin_url = reverse('%s:%s_%s_change'
                                % (admin_site.name,
                                   opts.app_label,
                                   opts.object_name.lower()),
                                None, (quote(obj._get_pk_val()),))
            p = '%s.%s' % (opts.app_label,
                           opts.get_delete_permission())
            if not user.has_perm(p):
                perms_needed.add(opts.verbose_name)
            p = '%s.%s' % (opts.app_label,
                           opts.get_change_permission())
            if not user.has_perm(p):
                perms_needed.add(opts.verbose_name)
            p = '%s.%s' % (opts.app_label,
                           opts.get_add_permission())
            if not user.has_perm(p):
                perms_needed.add(opts.verbose_name)
            # Display a link to the admin page.
            return mark_safe(u'%s: <a href="%s">%s</a>' %
                             (escape(capfirst(opts.verbose_name)),
                              admin_url,
                              escape(obj)))
        else:
            # Don't display link to edit, because it either has no
            # admin or is edited inline.
            return u'%s: %s' % (capfirst(opts.verbose_name),
                                force_unicode(obj))

    to_merge = collector.nested(format_callback)

    protected = [format_callback(obj) for obj in collector.protected]

    return to_merge, perms_needed, protected
