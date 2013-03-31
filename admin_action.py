from zenshu.utils import UnicodeWriter, get_merged_objects
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.db import router
from django.utils.encoding import force_unicode
from django.template.response import TemplateResponse
from django.contrib.admin import helpers
from django.contrib import messages
from django.http import HttpResponse


def merge_selected(modeladmin, request, queryset):
    """
    Action which merges the selected objects.

    This action first displays a confirmation page whichs shows all the
    mergable objects, or, if the user has no permission one of the related
    childs (foreignkeys), a "permission denied" message.

    Next, it merge all selected objects and redirects back to the change list.
    """
    if (queryset and (1 < queryset.all().count())):
        opts = modeladmin.model._meta
        app_label = opts.app_label

        # Check that the user has permission for the actual model
        if not modeladmin.has_delete_permission(request):
            raise PermissionDenied
        if not modeladmin.has_change_permission(request):
            raise PermissionDenied
        if not modeladmin.has_add_permission(request):
            raise PermissionDenied

        using = router.db_for_write(modeladmin.model)

        # Populate meragable, a data structure of all related objects that
        # will also be merged.
        mergeable_objects, perms_needed, protected = get_merged_objects(
            queryset, opts, request.user, modeladmin.admin_site, using)

        # The user has already confirmed the mergeration.
        # Do the mergeration and return a None to
        # display the change list view again.
        if request.POST.get('post'):
            if perms_needed:
                raise PermissionDenied
            n = queryset.count()
            if n:
                merge_function = 'merge_selected_' + opts.object_name.lower()
                merge_function = globals()[merge_function]
                if (merge_function(modeladmin, request, queryset)):
                    messages.success(request, _("Merge Completed"))
            # Return None to display the change list page again.
            return None

        if len(queryset) == 1:
            objects_name = force_unicode(opts.verbose_name)
        else:
            objects_name = force_unicode(opts.verbose_name_plural)

        if perms_needed or protected:
            title = _("Cannot merge %(name)s") % {"name": objects_name}
        else:
            title = _("Are you sure?")

        context = {
            "title": title,
            "objects_name": objects_name,
            "mergeable_objects": [mergeable_objects],
            'queryset': queryset,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": opts,
            "app_label": app_label,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }

        # Display the confirmation page
        templates = ["admin/%s/%s/merge_selected_confirmation.html"
                     % (app_label, opts.object_name.lower()),
                     "admin/%s/merge_selected_confirmation.html" % app_label,
                     "admin/merge_selected_confirmation.html"
                     ]
        return TemplateResponse(request,
                                templates,
                                context,
                                current_app=modeladmin.admin_site.name)
    else:
        messages.error(request, _("Please select at least two objects"))

merge_selected.short_description = _("Merge selected %(verbose_name_plural)s")


def prep_field(obj, field):
    """ Returns the field as a unicode string. If the field is a callable, it
    attempts to call it first, without arguments.
    """
    if '__' in field:
        bits = field.split('__')
        field = bits.pop()

        for bit in bits:
            obj = getattr(obj, bit, None)

            if obj is None:
                return ""

    attr = getattr(obj, field)
    output = attr() if callable(attr) else attr
#    return unicode(output).encode('utf-8') if output else ""
    return output


def export_csv_action(description=_("Export Selected %(verbose_name_plural)s"),
                      fields=None,
                      exclude=None,
                      header=True):
    """ This function returns an export csv action. """
    def export_as_csv(modeladmin, request, queryset):
        """ Generic csv export admin action.
        Based on http://djangosnippets.org/snippets/2712/
        """
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]
        labels = []

        if exclude:
            field_names = [f for f in field_names if f not in exclude]

        elif fields:
            field_names = [field for field, _ in fields]
            labels = [label for _, label in fields]

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
            unicode(opts).replace('.', '_')
        )

        writer = UnicodeWriter(response)

        if header:
            writer.writerow(labels if labels else field_names)

        for obj in queryset:
            writer.writerow([prep_field(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv
