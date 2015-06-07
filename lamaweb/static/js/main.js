
function modal(url, size) {
    size = (typeof size == 'undefined' ? '' : size);
    var dialog = $('#modal .modal-dialog').removeClass().addClass('modal-dialog');
    if (size != '')
	dialog.addClass('modal-' + size);
    $.get('/ajax/' + url, function(data) {
	$('#modal .modal-content').html(data);
	$('#modal').modal('show');
	modalHandler();
    }).fail(function() {
	alert('A gigantic internet monster destroyed everything. Please try again.');
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

function mapHandler() {
    var layers = [
	new ol.layer.Tile({
	    source: new ol.source.MapQuest({layer: 'osm'}),
	}),
    ];
    if (typeof itinerary != 'undefined') {
	layers.push(new ol.layer.Tile({
	    source: new ol.source.XYZ({
		url: apiitiurl + '/itineraries/' + itinerary.id + '/tiles/{z}/{x}/{y}',
		crossOrigin: 'null'
	    })
	}));
	var icons = [coordinateToIcon(itinerary.departure, '/static/departure.png')];
	for (i in itinerary.destinations) {
	    icons.push(coordinateToIcon(itinerary.destinations[i], '/static/arrival.png'));
	}
	var iconsLayer = new ol.layer.Vector({
	    source: new ol.source.Vector({
		features: icons
	    })
	});
	layers.push(iconsLayer);
    }
    var mapView = new ol.View({
	center: [260791.0276881127, 6249673.658616584],
	zoom: 13.8,
    });
    var map = new ol.Map({
	target: 'map',
	layers: layers,
	view: mapView
    });
    var extent = [itinerary.destinations[0].longitude,
		  itinerary.destinations[0].latitude,
		  itinerary.departure.longitude,
		  itinerary.departure.latitude];
    extent = ol.extent.applyTransform(extent, ol.proj.getTransform("EPSG:4326", "EPSG:3857"));
    mapView.fitExtent(extent, map.getSize());
    return map;
}

heightHandler();
$(window).resize(function() {
    heightHandler();
});

modalHandler();
var hash = window.location.hash.substring(1);
if (hash != '') {
    var a = $('#navbar-toggler a[href=#' + hash + ']');
    if (a.length > 0) {
	modal(hash, a.attr('data-size'));
    }
}
map = mapHandler();
