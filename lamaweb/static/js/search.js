
function newDestinationElement(index) {
    var newTemplate = $($("#destination-template").html());
    var input = newTemplate.find('input');
    input.attr('name', 'destination-' + index);
    input.attr('data-index', index);
    if (typeof itinerary != 'undefined' && typeof itinerary.destinations[index] != 'undefined') {
	input.val(coordinateToString(itinerary.destinations[index]));
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
    $('a[href="#addDestination"]').show();
}

function reloadMapIcons() {
    // remove incidents to avoid wrong extent
    removeLayer('Incidents');
    // reload itinerary
    removeLayer('Itinerary');
    map.addLayer(itineraryLayer());
    // reload icons
    removeLayer('Icons');
    map.addLayer(iconsLayer());
    // zoom, center
    fitExtent();
    // re-display incidents
    map.addLayer(incidentsLayer());
}

function reloadDestinationsAndMap(new_itinerary) {
    itinerary = new_itinerary;
    reloadDestinations();
    reloadMapIcons();
}

function deleteHandler() {
    $('a[href="#deleteDestination"]').click(function(e) {
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
	$('a[href="#addDestination"]').hide();
    });
    $('a[href="#editDestination"]').click(function(e) {
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

	$('a[href="#editDeparture"]').click(function(e) {
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
			input.val(coordinateToString(itinerary.departure));
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

	$('a[href="#editVehicle"]').click(function(e) {
	    e.preventDefault();
	    var selected_vehicle = $('select[name=vehicle]').val();
	    if (selected_vehicle != parseInt(itinerary.vehicle)) {
		$.ajax({
		    type: 'POST',
		    url: '/ajax/form/editvehicle',
		    data: {
			'itinerary': itinerary.id,
			'vehicle': selected_vehicle,
		    },
		    success: function(new_itinerary) {
			itinerary = new_itinerary;
			$('select[name=vehicle]').val(itinerary.vehicle);
			$('.cuteform-selected').removeClass('cuteform-selected');
			$('[data-cuteform-val=' + itinerary.vehicle + ']').addClass('cuteform-selected');
			reloadMapIcons();
		    },
		    error: genericAjaxError,
		    dataType: 'json',
		});
	    }
	    return false;
	});

	$('a[href="#addDestination"]').click(function(e) {
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
	$('a[href="#addDestination"]').click(function(e) {
	    e.preventDefault();
	    var lastIndex = $('#destinations').find('.destination').last().find('input').attr('data-index');
	    $('#destinations').append(newDestinationElement(parseInt(lastIndex) + 1));
	});
    }
});
