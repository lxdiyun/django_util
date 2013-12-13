from django.views.generic import DetailView
from django.views.generic.base import ContextMixin
from django.conf import settings
from django.contrib.gis.maps.google.gmap import GoogleMapException


class GmapContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(GmapContextMixin, self).get_context_data(**kwargs)
        try:
            key = settings.GOOGLE_MAPS_API_KEY
        except AttributeError:
            raise GoogleMapException('Google Maps API Key not found (try '
                                     'adding GOOGLE_MAPS_API_KEY to your '
                                     'settings).')

        context['GOOGLE_MAPS_API_KEY'] = key

        try:
            url = settings.GOOGLE_MAPS_API_URL
        except AttributeError:
            raise GoogleMapException('Google Maps API URL not found (try '
                                     'adding GOOGLE_MAPS_API_URL to your '
                                     'settings).')

        context['GOOGLE_MAPS_API_URL'] = url

        return context


class DetailViewWithGmap(DetailView, GmapContextMixin):
    pass
