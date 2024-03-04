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
            // Display the list of users in a table with 3 columns
            var table = $('<table>').addClass('user-table');

            for (var i = 0; i < users.length; i += 3) {
                // Create a table row for every 3 users
                var row = $('<tr>');

                // Iterate over the next 3 users
                for (var j = i; j < i + 3 && j < users.length; j++) {
                    // Create a table cell for each user
                    var cell = $('<td>');

                    // Create a circular image with reduced size
                    var userCard = $('<div>').addClass('user-card');
                    var profileLink = $('<a>').attr('href', '/profile?user_id=' + users[j][2]);

                    // Create a div for the profile picture
                    var profilePictureDiv = $('<div>').addClass('profile-picture-circle');
                    var image = $('<img>')
                        .attr('src', users[j][1] || 'uploads/default.png')
                        .attr('alt', users[j][0]);
                    profilePictureDiv.append(image);
                    profileLink.append(profilePictureDiv);

                    // Append the profile picture to the user card
                    userCard.append(profileLink);

                    // Append the username below the profile picture
                    userCard.append($('<span>').text(users[j][0]));

                    // Append the user card to the table cell
                    cell.append(userCard);

                    // Append the table cell to the table row
                    row.append(cell);
                }

                // Append the table row to the table
                table.append(row);
            }

            // Append the table to the search results
            searchResultsDiv.append(table);
        } else {
            // Display a message for no results
            searchResultsDiv.text('No users found.');
        }
    }
});
