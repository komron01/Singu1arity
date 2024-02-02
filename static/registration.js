// registration.js

$(document).ready(function () {
    $('#username').on('blur', function () {
        var username = $(this).val();

        // Perform an AJAX request to check username availability
        $.ajax({
            url: '/check-username',  
            method: 'POST',
            data: { 'username': username },
            success: function (response) {
                var availabilityDiv = $('#usernameAvailability');

                if (response.available) {
                    availabilityDiv.text('Username is available').css('color', 'green');
                } else {
                    availabilityDiv.text('Username is already taken').css('color', 'red');
                }
            }
        });
    });
});
