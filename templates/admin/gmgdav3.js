{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}new OpenLayers.Layer.Google("Google Base Layer", {'type': google.maps.MapTypeId.ROADMAP, 'sphericalMercator' : true});{% endblock %}

{% block controls %}
django.jQuery(document).ready(function() {

	var mappa = {{ module }}.map;
	var lng, lat
	var $address = django.jQuery('#id_address');

$address.change(function() {
	if (!django.jQuery("#id_longitude").val()) {
		geocod($address.val(), mappa);
	}
});

django.jQuery('#id_longitude, #id_latitude').change(function() {
	lng = django.jQuery("#id_longitude").val();
	lat = django.jQuery("#id_latitude").val();
	modcoo(lng, lat, mappa);
	revgeocod(lng, lat, mappa); 
});

});

function modcoo(lng, lat, mappa) {
	mappa.setCenter(new OpenLayers.LonLat(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")), 13);
	var c = new OpenLayers.Geometry.Point(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
	{{ module }}.layers.vector.addFeatures([new OpenLayers.Feature.Vector(c)]);
}

function input_lng_lat(lng, lat, mappa) {
	django.jQuery("#id_longitude").val(lng.toFixed(6));
	django.jQuery("#id_latitude").val(lat.toFixed(6));
}

function geocod(ind, mappa) {
	var geocoder = new google.maps.Geocoder();
	geocoder.geocode({'address': ind} ,
			 function(results,status) { 
				 if (status == google.maps.GeocoderStatus.OK) {
					 if (status != google.maps.GeocoderStatus.ZERO_RESULTS) {
						 lat = results[0].geometry.location.lat();  
						 lng = results[0].geometry.location.lng(); 
						 mappa.setCenter(new OpenLayers.LonLat(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")), 13);
						 var c = new OpenLayers.Geometry.Point(lng,lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
						 {{ module }}.layers.vector.addFeatures([new OpenLayers.Feature.Vector(c)]);
						 input_lng_lat(lng, lat, mappa);
					 }	
				 }
				 else {
					 alert("Address not found!");
				 }
			 }
			)  
};

function revgeocod(lng, lat, mappa) {
	var geocoder = new google.maps.Geocoder();
	var infowindow = new google.maps.InfoWindow();
	var latlng = new google.maps.LatLng(lat,lng);
	geocoder.geocode({'latLng': latlng}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			django.jQuery("#id_address").val(results[0].formatted_address);
		} else {
			alert("Geocoder failed due to: " + status);
		}
	});
};

{{ module }}.drawPointHandler = function () { 
	srco = document.getElementById('{{ id }}').value;
	var mappa = {{ module }}.map;
	var a = srco.split(" ");
	var b = a[0].split("(");
	var c = a[1].split(")");
	lngm = parseFloat(c[0]);
	latm = parseFloat(b[1]);
	var c = new OpenLayers.Geometry.Point(latm,lngm).transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"));
	input_lng_lat(c.x,c.y, mappa);
	revgeocod(c.x, c.y, mappa);
};


// Create an array of controls based on geometry type
{{ module }}.getControls = function(lyr){
  {{ module }}.panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
  var nav = new OpenLayers.Control.Navigation();
  var draw_ctl;
  if ({{ module }}.is_point){
    draw_ctl = new OpenLayers.Control.DrawFeature(lyr, OpenLayers.Handler.Point, {
	    'displayClass': 'olControlDrawFeaturePoint',
    });
    draw_ctl.events.register('featureadded', draw_ctl, function(f) {
	    {{ module }}.drawPointHandler()
    });
  }
  if ({{ module }}.modifiable){
    var mod = new OpenLayers.Control.ModifyFeature(lyr, {'displayClass': 'olControlModifyFeature'});
    {{ module }}.controls = [nav, draw_ctl, mod];
  } else {
    if(!lyr.features.length){
      {{ module }}.controls = [nav, draw_ctl];
    } else {
      {{ module }}.controls = [nav];
    }
  }
}

{{ block.super }}

{% endblock %}
