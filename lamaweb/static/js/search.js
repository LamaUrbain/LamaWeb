
function newDestinationElement(index) {
    var newTemplate = $($("#destination-template").html());
    var input = newTemplate.find('input');
    input.attr('name', 'destination-' + index);
    input.attr('data-index', index);
    if (typeof itinerary != 'undefined' && typeof itinerary.destinations[index] != 'undefined') {
	if (itinerary.destinations[index].address) {
	    input.val(itinerary.destinations[index].address);
	} else if (itinerary.destinations[index].latitude) {
	    input.val(itinerary.destinations[index].latitude + ',' + itinerary.destinations[index].longitude);
	}
    }
    input.attr('data-old-destination', input.val());
    $("#destinations").append(newTemplate);
}

function reloadDestinations() {
    $("#destinations").html('');
    for (i in itinerary.destinations) {
	$("#destinations").append(newDestinationElement(i));
    }
    destinationsHandler();
    $('a[href=#addDestination]').show();
}

function reloadMapIcons() {
    // reload itinerary
    removeLayer('Itinerary');
    map.addLayer(itineraryLayer());
    // reload icons
    removeLayer('Icons');
    map.addLayer(iconsLayer());
    // zoom, center
    fitExtent();
}

function reloadDestinationsAndMap(new_itinerary) {
    itinerary = new_itinerary;
    reloadDestinations();
    reloadMapIcons();
}

function deleteHandler() {
    $('a[href=#deleteDestination]').click(function(e) {
	e.preventDefault();
	var deleteButton = $(this);
	if (deleteButton.closest('.destination').find('input').val() == "") {
	    reloadDestinations();
	} else {
	    $.ajax({
		type: 'POST',
		url: '/ajax/form/deletedestination',
		data: {
		    'itinerary': itinerary.id,
		    'position': deleteButton.closest('.destination').find('input').attr('data-index')
		},
		success: reloadDestinationsAndMap,
		error: genericAjaxError,
		dataType: 'json'
	    });
	}
    });
}

function editHandler() {
    $('#destinations .destination input').focus(function(e) {
	$('#destinations .delete-destination').hide();
	$(this).closest('.destination').find('.edit-destination').show();
	$('a[href=#addDestination]').hide();
    });
    $('a[href=#editDestination]').click(function(e) {
	var editButton = $(this);
	var destinationBar = $(this).closest('.destination');
	var input = destinationBar.find('input');
	if (input.val() == input.attr('data-old-destination')) {
	    reloadDestinations();
	} else if (input.attr('data-old-destination') == "") {
	    $.ajax({
		type: 'POST',
		url: '/ajax/form/adddestination',
		data: {
		    'itinerary': itinerary.id,
		    'destination': input.val()
		},
		success: reloadDestinationsAndMap,
		error: genericAjaxError,
		dataType: 'json'
	    });
	} else {
	    $.ajax({
		type: 'POST',
		url: '/ajax/form/editdestination',
		data: {
		    'itinerary': itinerary.id,
		    'position': input.attr('data-index'),
		    'destination': input.val()
		},
		success: reloadDestinationsAndMap,
		error: genericAjaxError,
		dataType: 'json'
	    });
	}
    });
}

function destinationsHandler() {
    deleteHandler();
    editHandler();
}

function resetDeparture() {
    $('#departure').find('.col-xs-10').addClass('col-xs-12').removeClass('col-xs-10');
    $('#departure').find('.col-xs-2').hide();
}

$(document).ready(function() {

    if (typeof itinerary != 'undefined') {
	$('#departure input').focus(function(e) {
	    $('#departure').find('.col-xs-12').addClass('col-xs-10').removeClass('col-xs-12');
	    $('#departure').find('.col-xs-2').show();
	});

	$('#departure input').attr('data-old-destination', $('#departure input').val());

	$('a[href=#editDeparture]').click(function(e) {
	    var input = $('#departure input');
	    if (input.val() == input.attr('data-old-destination')) {
		resetDeparture();
	    } else if (input.val() != "") {
		$.ajax({
		    type: 'POST',
		    url: '/ajax/form/edititinerary',
		    data: {
			'itinerary': itinerary.id,
			'departure': input.val()
		    },
		    success: function(new_itinerary) {
			itinerary = new_itinerary;
			if (itinerary.departure.address) {
			    input.val(itinerary.departure.address);
			} else if (itinerary.departure.latitude) {
			    input.val(itinerary.departure.latitude + ',' + itinerary.departure.longitude);
			}
			resetDeparture();
			reloadMapIcons();
		    },
		    error: genericAjaxError,
		    dataType: 'json'
		});
		$('departure')
		resetDeparture();
	    }
	});

	$('a[href=#addDestination]').click(function(e) {
	    e.preventDefault();
	    var lastIndex = $('#destinations').find('.destination').last().find('input').attr('data-index');
	    $('#destinations').append(newDestinationElement(parseInt(lastIndex) + 1));
	    $(this).hide();
	    destinationsHandler();
	});

	destinationsHandler();
    } else {
	$('button[name=search]').click(function(e) {
	    e.preventDefault();
	    $('#searchform').submit();
	});
	$('a[href=#addDestination]').click(function(e) {
	    e.preventDefault();
	    var lastIndex = $('#destinations').find('.destination').last().find('input').attr('data-index');
	    $('#destinations').append(newDestinationElement(parseInt(lastIndex) + 1));
	});
    }
});
