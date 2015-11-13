var map = 0;
var mapView = 0;
var popup = 0;
var incidents = 0;

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

function coordinateToString(coordinate) {
    if (coordinate.address) {
	return coordinate.address;
    }
    return coordinate.latitude + ',' + coordinate.longitude;
}

function coordinateToIcon(coordinate, png, extraData) {
    var lonlat = ol.proj.fromLonLat([coordinate.longitude, coordinate.latitude]);
    var iconFeature = new ol.Feature({
	geometry: new ol.geom.Point(lonlat),
	name: coordinate.address,
	coordinateObject: coordinate,
	extraData: extraData,
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

function incidentsLayer() {
    var incident, icons = [];
    for (idx in incidents) {
	incident = incidents[idx];
	icons.push(coordinateToIcon(incident['position'], '/static/incident.png', incident))
    }
    var incidentsVector = new ol.source.Vector({
	features: icons
    });
    var incidentsLayer = new ol.layer.Vector({
	source: incidentsVector,
	name: 'Incidents'
    });
    return incidentsLayer;
}

function getIncidents() {
    $.get(apiurl + '/incidents', function(data) {
	incidents = data;
	map.addLayer(incidentsLayer());
    });
}

function initPopup() {
    var element = $('#popup');
    popup = new ol.Overlay({
	element: element,
	positioning: 'bottom-center',
	stopEvent: false
    });
    map.addOverlay(popup);
    var element = $('#popup')
    map.on('click', function(evt) {
	var feature = map.forEachFeatureAtPixel(evt.pixel,
						function(feature, layer) {
						    return feature;
						});
	if (feature && typeof(feature.get('extraData')) != 'undefined') {
	    popup.setPosition(evt.coordinate);
	    element.popover({
		'placement': 'top',
		'html': true,
		'container': $('#map'),
		'title': feature.get('extraData')['name'],
		'content': (feature.get('extraData')['end'] != null ?
			    'Ends: ' + feature.get('extraData')['end'] + '<br>' : '')
		    + coordinateToString(feature.get('coordinateObject')),
	    });
	    element.popover('show');
	} else {
	    element.popover('destroy');
	}
    });
    map.getViewport().addEventListener('contextmenu', function (e) {
	e.preventDefault();
	var coordinate = map.getEventCoordinate(e);
	var lonlat = ol.proj.transform(coordinate, 'EPSG:3857', 'EPSG:4326');
	popup.setPosition(coordinate);
	$('#reportform-wrapper input[name=position]').val(lonlat[1] + ',' + lonlat[0]);
	element.popover({
	    'placement': 'top',
	    'html': true,
	    'container': $('#map'),
	    'title': 'Report incident here',
	    'content': $('#reportform-wrapper').html(),
	});
	element.popover('show');
    });
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
    initPopup();
    fitExtent();
    // called after extent to avoid wrong extent
    getIncidents();
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
