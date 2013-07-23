from django.contrib.gis.db import models
from django.utils.encoding import smart_unicode
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Point(models.Model):
    address = models.CharField(max_length=100,
                               help_text='Press "Tab" to refresh the map')
    longitude = models.FloatField(help_text='WGS84 Decimal Degree. '
                                  'Press "Tab" to refresh the map')
    latitude = models.FloatField(help_text='WGS84 Decimal Degree. '
                                 'Press "Tab" to refresh the map')
    in_geom = models.PointField('shp', srid=4326)
    photos = generic.GenericRelation('Photo',
                                     content_type_field='content_type',
                                     object_id_field='object_id')

    objects = models.GeoManager()

    def __unicode__(self):
        return smart_unicode(self.address)


class Photo(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('photo name'))
    image = models.ImageField(upload_to='utils_photo',
                              verbose_name=_('Image'))
    thumbnail = ImageSpecField(source='image',
                               processors=[SmartResize(75, 100)],
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
