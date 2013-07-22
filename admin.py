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
    try:
        url = settings.GOOGLE_MAPS_API_URL
    except AttributeError:
        raise GoogleMapException('Google Maps API URL not found (try '
                                 'adding GOOGLE_MAPS_API_URL to your '
                                 'settings).')
    g = GEOSGeometry('POINT (116.71 23.37)')  # Set map center
    g.set_srid(4326)
    g.transform(900913)
    default_lon = int(g.x)
    default_lat = int(g.y)
    default_zoom = 13
    extra_js = [url + "?key=" + key + "&sensor=false&language=zh-CN"]
    openlayers_url = "http://openlayers.org/api/2.13.1/OpenLayers.js"
    print extra_js
    map_template = 'admin/gmgdav3.html'

admin.site.register(Point, GoogleAdmin)
