
$('#settingsform').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    $('.saved-message').hide();
    $.ajax({
	type: 'POST',
	url: form.attr('action'),
	data: {
	    'email': form.find('input[name=email]').val(),
	    'password': form.find('input[name=password]').val(),
	},
	success: function(data) {
	    $('.saved-message').show('fast');
	},
	error: genericAjaxError
    });
    return false;
});
