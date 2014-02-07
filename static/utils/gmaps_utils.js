var map;
var g_bounds_min_zoom = null;
function load_map() {
	var mapOption = { 
		div: '#map', 
		zoom: 12,
		lat: 23.37, 
		lng: 116.71,
		streetViewControl: false,
		overviewMapControl: false,
		panControl: false,
		scaleControl: true,
		scaleControlOptions: {
			position: google.maps.ControlPosition.RIGHT_BOTTOM
		},
		mapTypeControl: true,
		mapTypeControlOptions: {
			style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
			position: google.maps.ControlPosition.TOP_LEFT
		},
		zoomControl: true,
		zoomControlOptions: {
			position: google.maps.ControlPosition.TOP_RIGHT
		},
	};
	map = new GMaps(mapOption);

	if (null != g_bounds_min_zoom) {
		google.maps.event.addListener(map.map, 'zoom_changed', function() {
			zoomChangeBoundsListener = 
			google.maps.event.addListener(map.map, 'bounds_changed', function(event) {
				if (this.getZoom() > g_bounds_min_zoom) {
					// Change max/min zoom here
					this.setZoom(g_bounds_min_zoom);
				}
				google.maps.event.removeListener(zoomChangeBoundsListener);
			});
		});
	}
}

var markers = [];
function add_marker(id, lat, lng, title, call_back, infowindow_group) {
	var infowindow = null;
	if (typeof(infowindow_group)==='undefined') {
		infowindow = new google.maps.InfoWindow();
	} else {
		infowindow = infowindow_group;
	}
	var marker = GMaps.prototype.createMarker({ 
		lat: lat,
	    lng: lng,
	    title: title,
	    animation: google.maps.Animation.DROP
	});
	marker.id = id;
	markers.push(marker);
	map.addMarker(marker);

	google.maps.event.addListener(marker, 'click', function() {
		infowindow.setContent(marker.title);
		infowindow.open(marker.get('map'), marker);
		if ((typeof(call_back)!=='undefined') && (null !== call_back)) {
			call_back(marker);
		}
	});
}

function set_all_map(map) {
	for (var i = 0; i < markers.length; i++) {
		markers[i].setMap(map);
	}
}

function clean_all_markers() {
	set_all_map(null);
	markers.length = 0;
}

function zoom_to_show_all_markers(data) {
	//  Create a new viewpoint bound
	var bounds = new google.maps.LatLngBounds ();
	//  Go through each...
	for (i = 0, markers_length = markers.length; i < markers_length; ++i) {
		bounds.extend(markers[i].getPosition());
	}
	//  Fit these bounds to the map
	map.fitBounds (bounds);
}
