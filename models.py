from uuid import uuid4
import os

from django.contrib.gis.db import models
from django.utils.encoding import smart_unicode
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class PointBase(models.Model):
    address = models.CharField(max_length=100,
                               help_text='Press "Tab" to refresh the map')
    longitude = models.FloatField(help_text='WGS84 Decimal Degree. '
                                  'Press "Tab" to refresh the map')
    latitude = models.FloatField(help_text='WGS84 Decimal Degree. '
                                 'Press "Tab" to refresh the map')
    in_geom = models.PointField('shp', srid=4326)

    objects = models.GeoManager()

    def __unicode__(self):
        return smart_unicode(self.address)

    class Meta:
        abstract = True


def random_path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper


class PhotoBase(models.Model):
    thumbnail_width, thumbnail_height = 75, 100
    name = models.CharField(max_length=250, verbose_name=_('photo name'))
    image = models.ImageField(upload_to=random_path_and_rename('utils_photo'),
                              verbose_name=_('Image'))
    thumbnail = ImageSpecField(source='image',
                               processors=[SmartResize(thumbnail_width,
                                                       thumbnail_height)],
                               format='JPEG',
                               options={'quality': 60})
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
        abstract = True
