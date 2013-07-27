from django.contrib.gis import admin
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.maps.google.gmap import GoogleMapException
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from imagekit.admin import AdminThumbnail


class PhotoInlineBase(generic.GenericTabularInline):
    model = 'Photo'
    readonly_fields = ['admin_thumbnail']
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')

    admin_thumbnail.short_description = _('Thumbnail')


class PointAdminBase(admin.OSMGeoAdmin):
    try:
        key = settings.GOOGLE_MAPS_API_KEY
        key_url = "?key=" + key
    except AttributeError:
        key = ""
        key_url = "?"

    try:
        url = settings.GOOGLE_MAPS_API_URL
    except AttributeError:
        url = "https://maps.googleapis.com/maps/api/js"

    g = GEOSGeometry('POINT (116.71 23.37)')  # Set map center
    g.set_srid(4326)
    g.transform(900913)
    default_lon = int(g.x)
    default_lat = int(g.y)
    default_zoom = 13
    extra_js = [url + key_url + "&sensor=false&language=zh-CN"]
    openlayers_url = "http://openlayers.org/api/2.13.1/OpenLayers.js"
    map_template = 'admin/gmgdav3.html'


class PhotoAdmin(admin.ModelAdmin):
    list_display = ["name", "admin_thumbnail"]
    fields = ["name", "image", "admin_thumbnail"]
    readonly_fields = ['admin_thumbnail']
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    search_fields = ['name']

    admin_thumbnail.short_description = _('Thumbnail')
