
$('#map').height($(window).height());
$('nav').css('height', $(window).height());

$(window).resize(function() {
    $('#map').height($(window).height());
    $('nav').css('height', $(window).height());
});

var map = new ol.Map({
    target: 'map',
    layers: [
	new ol.layer.Tile({
	    source: new ol.source.MapQuest({layer: 'osm'})
	})
    ],
    view: new ol.View({
	center: [260791.0276881127, 6249673.658616584],
	zoom: 13.8
    })
});
