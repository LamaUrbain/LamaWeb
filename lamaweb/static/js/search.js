
function deleteHandler() {
    $('a[href=#deleteDestination]').click(function(e) {
	e.preventDefault();
	$(this).closest('.destination').remove();
    });
}

$(document).ready(function() {
    $('a[href=#addDestination]').click(function(e) {
	e.preventDefault();
	$('.destination').last().before('<div class="destination row"><div class="col-xs-10"><input type="text" class="form-control search" placeholder="Destination" name="point' + ($('.search').length + 1) + '"></div><div class="col-xs-2"><a class="btn btn-secondary" href="#deleteDestination"><i class="flaticon-delete"></i></a></div></div>');
	deleteHandler();
    });
    deleteHandler();
});

// TODO
// handle click on search / save button
// if save, call ajax form /ajax/save then refresh the map
// if search, just refresh the map
