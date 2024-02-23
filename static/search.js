// search.js

$(document).ready(function () {
    $('#searchLetter').on('input', function () {
        var searchLetter = $(this).val();

        // Perform an AJAX request to fetch users starting with the input letter
        $.ajax({
            url: '/search_user',
            method: 'GET',
            data: { 'letter': searchLetter },
            success: function (response) {
                displaySearchResults(response);
            }
        });
    });

    function displaySearchResults(users) {
        var searchResultsDiv = $('#searchResults');
        searchResultsDiv.empty();
    
        if (users.length > 0) {
            // Display the list of users
            var userList = $('<ul>');
            users.forEach(function (user) {
                var username = user[0];
                var profilePicture = user[1] || 'static/default.png';
    
                // Create a circular image with reduced size
                var listItem = $('<li>');
                var image = $('<img>')
                    .attr('src', profilePicture)
                    .attr('alt', username)
                    .addClass('profile-image'); // Add a class for styling
                listItem.append(image).append($('<span>').text(username));
                userList.append(listItem);
            });
            searchResultsDiv.append(userList);
        } else {
            // Display a message for no results
            searchResultsDiv.text('No users found.');
        }
    }
    
    
    
});
