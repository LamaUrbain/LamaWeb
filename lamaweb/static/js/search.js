
$(document).ready(function() {
    $('a[href=#addDestination]').click(function(e) {
	e.preventDefault();
	$('.search').last().attr('placeholder', 'Destination');
	$('.search').last().after('<input type="text" class="form-control search" placeholder="Destination" name="point' + ($('.search').length + 1) + '">');
    });
});
