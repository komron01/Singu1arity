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
            // Display the list of friends
            var friendsUl = $('<ul>');
            friends.forEach(function (friend) {
                // Create a list item for each friend
                var listItem = $('<li>');
    
                // Create a div for the friend container
                var friendContainer = $('<div>').addClass('friend-container');
    
                // Create a div for the profile picture
                var profilePictureDiv = $('<div>').addClass('profile-picture');
                var profilePicture = $('<img>').attr('src', friend[1] || 'static/default.png').attr('alt', 'Profile Picture');
                profilePictureDiv.append(profilePicture);
    
                // Create a div for the username
                var userInfoDiv = $('<div>').addClass('user-info');
                userInfoDiv.append($('<h4>').text(friend[0]));
    
                // Append the profile picture and username to the friend container
                friendContainer.append(profilePictureDiv, userInfoDiv);
    
                // Append the friend container to the list item
                listItem.append(friendContainer);
    
                // Append the list item to the friends list
                friendsUl.append(listItem);
            });
    
            // Append the list of friends to the friends list container
            friendsList.append(friendsUl);
        } else {
            // Display a message for no friends
            friendsList.text('No friends found.');
        }
    }
    
    

    // ... the rest of your code
});
