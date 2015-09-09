
$(document).ready(function() {
    // handle delete form on click on delete button
    $('button[name=deleteItinerary]').click(function(e) {
	e.preventDefault();
	var button = $(this);
	var form = button.closest('form');
	var itinerary_id = form.find('input[name=itinerary]').val();
	$.ajax({
	    type: 'POST',
	    url: '/ajax/form/deleteitinerary',
	    data: {
		'itinerary': itinerary_id,
	    },
	    success: function(data) {
		// on success, delete the table row that corresponds to the deleted itinerary
		button.closest('tr').prev().remove();
		button.closest('tr').remove();
	    },
	    error: genericAjaxError,
	});
	return false;
    });
});
