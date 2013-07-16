from models import Point
from django.contrib.gis import admin
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.maps.google.gmap import GoogleMapException
from django.conf import settings


class GoogleAdmin(admin.OSMGeoAdmin):
    try:
        key = settings.GOOGLE_MAPS_API_KEY
    except AttributeError:
        raise GoogleMapException('Google Maps API Key not found (try '
                                 'adding GOOGLE_MAPS_API_KEY to your '
                                 'settings).')
    g = GEOSGeometry('POINT (9.191884 45.464254)')  # Set map center
    g.set_srid(4326)
    g.transform(900913)
    default_lon = int(g.x)
    default_lat = int(g.y)
    default_zoom = 7
    extra_js = ["http://ditu.google.cn/maps/api/js?"
                "key=" + key +
                "&sensor=false&language=zh-CN"]
    print extra_js
    map_template = 'admin/gmgdav3.html'

admin.site.register(Point, GoogleAdmin)
