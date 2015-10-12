var map = 0;
var mapView = 0;

function genericAjaxError(xhr, status, error) {
    alert(eval("(" + xhr.responseText + ")").error);
}

function modal(url, size, silent) {
    size = (typeof size == 'undefined' ? '' : size);
    silent = (typeof silent == 'undefined' ? false : silent);
    var dialog = $('#modal .modal-dialog').removeClass().addClass('modal-dialog');
    if (size != '')
	dialog.addClass('modal-' + size);
    $.get('/ajax/' + url, function(data) {
	$('#modal .modal-content').html(data);
	$('#modal').modal('show');
	modalHandler();
    }).fail(function() {
	if (!silent) {
	    alert('A gigantic internet monster destroyed everything. Please try again.');
	}
    });
}

function modalHandler() {
    $('a[data-toggle=ajaxmodal]').click(function(e) {
	modal($(this).attr('href').replace('#', ''), $(this).attr('data-size'));
    });
    $('[data-toggle="tooltip"]').tooltip()
}

function heightHandler() {
    $('#map').height($(window).height());
    $('nav').css('height', $(window).height());
}

function coordinateToIcon(coordinate, png) {
    var lonlat = ol.proj.fromLonLat([coordinate.longitude, coordinate.latitude]);
    var iconFeature = new ol.Feature({
	geometry: new ol.geom.Point(lonlat),
	name: coordinate.address,
    });
    var iconStyle = new ol.style.Style({
	image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
	    anchor: [0.5, 46],
	    anchorXUnits: 'fraction',
	    anchorYUnits: 'pixels',
	    opacity: 1,
	    src: png
	}))
    });
    iconFeature.setStyle(iconStyle);
    return iconFeature
}

function getLayer(name) {
    var layers = map.getLayers();
    var theLayer = 0;
    layers.forEach(function(layer) {
	if (layer.get('name') == name) {
	    theLayer = layer;
	}
    });
    return theLayer;
}

function removeLayer(name) {
    var layer = getLayer(name);
    if (layer != 0) {
	map.removeLayer(layer);
    }
}

function iconsVector() {
    var icons = [coordinateToIcon(itinerary.departure, '/static/departure.png')];
    for (i in itinerary.destinations) {
	icons.push(coordinateToIcon(itinerary.destinations[i], '/static/arrival.png'));
    }
    var iconsVector = new ol.source.Vector({
	features: icons
    });
    return iconsVector
}

function iconsLayer() {
    var iconsLayer = new ol.layer.Vector({
	source: iconsVector(),
	name: 'Icons'
    });
    return iconsLayer
}

function getExtent() {
    var north = itinerary.departure.latitude;
    var south = itinerary.departure.latitude;
    var west = itinerary.departure.longitude;
    var east = itinerary.departure.longitude;
    for (i in itinerary.destinations) {
	var dest = itinerary.destinations[i];
	if (dest.latitude < north) {
	    north = dest.latitude;
	}
	if (dest.latitude > south) {
	    south = dest.latitude;
	}
	if (dest.longitude < west) {
	    west = dest.longitude;
	}
	if (dest.longitude > east) {
	    east = dest.longitude;
	}
    }
    return [west, north, east, south];
}

function fitExtent() {
    if (typeof itinerary != 'undefined') {
	var extent = getExtent();
	extent = ol.extent.applyTransform(extent, ol.proj.getTransform("EPSG:4326", "EPSG:3857"));
	mapView.fitExtent(extent, map.getSize());
    }
}

function itineraryLayer () {
    var itineraryLayerSource = new ol.source.XYZ({
	url: apiurl + '/itineraries/' + itinerary.id + '/tiles/{z}/{x}/{y}' + '?time=' + new Date().getTime(),
	crossOrigin: 'null',
	name: 'Itinerary'
    });
    return (new ol.layer.Tile({
	source: itineraryLayerSource,
	name: 'Itinerary'
    }));
}

function mapHandler() {
    var layers = [
	new ol.layer.Tile({
	    source: new ol.source.MapQuest({layer: 'osm'}),
	}),
    ];
    if (typeof itinerary != 'undefined') {
	layers.push(itineraryLayer());
	layers.push(iconsLayer());
    }
    mapView = new ol.View({
	center: [260791.0276881127, 6249673.658616584],
	zoom: 13.8,
	maxZoom: 16
    });
    map = new ol.Map({
	target: 'map',
	layers: layers,
	view: mapView
    });
    fitExtent();
    return [map, mapView];
}

heightHandler();
$(window).resize(function() {
    heightHandler();
});

modalHandler();
var hash = window.location.hash.substring(1);
if (hash != '') {
    var a = $('#navbar-toggler a[href="#' + hash + '"]');
    if (a.length > 0) {
	modal(hash, a.attr('data-size'));
    } else {
	modal(hash, 'lg', true);
    }
}
mapHandler();
