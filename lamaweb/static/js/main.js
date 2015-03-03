
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

function mapHandler() {
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
mapHandler();
