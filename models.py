from django.contrib.gis.db import models
from django.utils.encoding import smart_unicode


class Point(models.Model):
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
