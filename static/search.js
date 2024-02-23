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
                userList.append($('<li>').text(user.username));
            });
            searchResultsDiv.append(userList);
        } else {
            // Display a message for no results
            searchResultsDiv.text('No users found.');
        }
    }
});
