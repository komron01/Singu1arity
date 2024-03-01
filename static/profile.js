$(document).ready(function () {
    // Fetch friends for the current user
    fetchUserFriends();

    function fetchUserFriends() {
        var userId = $('#userId').data('user-id');

        // Perform an AJAX request to fetch user friends
        $.ajax({
            url: '/get_friends/' + userId,
            method: 'GET',
            success: function (response) {
                displayUserFriends(response);
            },
            error: function (error) {
                console.error('Error fetching friends:', error);
            }
        });
    }

    function displayUserFriends(friends) {
        var friendsList = $('#friendsList');
        friendsList.empty();
    
        if (friends.length > 0) {
            // Display the list of friends in a table
            var table = $('<table>');
    
            for (var i = 0; i < friends.length; i += 3) {
                // Create a table row for every 3 friends
                var row = $('<tr>');
    
                // Iterate over the next 3 friends
                for (var j = i; j < i + 3 && j < friends.length; j++) {
                    // Create a table cell for each friend
                    var cell = $('<td>');
    
                    // Create a div for the friend container
                    var friendContainer = $('<div>').addClass('friend-container');
    
                    // Create a div for the profile picture
                    var profilePictureDiv = $('<div>').addClass('profile-picture-circle');
                    var profilePicture = $('<img>').attr('src', friends[j][1] || 'uploads/default.png').attr('alt', 'Profile Picture');
                    profilePictureDiv.append(profilePicture);
    
                    // Append the profile picture to the friend container
                    friendContainer.append(profilePictureDiv);
    
                    // Create a div for the username
                    var userInfoDiv = $('<div>').addClass('user-info');
                    userInfoDiv.append($('<h4>').text(friends[j][0]));
    
                    // Append the username to the friend container
                    friendContainer.append(userInfoDiv);
    
                    // Append the friend container to the table cell
                    cell.append(friendContainer);
    
                    // Append the table cell to the table row
                    row.append(cell);
                }
    
                // Append the table row to the table
                table.append(row);
            }
    
            // Append the table to the friends list
            friendsList.append(table);
        } else {
            // Display a message for no friends
            friendsList.text('No friends found.');
        }
    }
    
    
    
    

    // ... the rest of your code
});
