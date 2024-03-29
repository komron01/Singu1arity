$(document).ready(function () {
    // Fetch and display posts when the page loads
    fetchAndDisplayPosts();
});

function fetchAndDisplayPosts() {
    // Perform an AJAX request to fetch feed posts
    $.ajax({
        url: '/get_posts_wall',  // Use the correct endpoint for fetching feed posts
        method: 'GET',
        success: function (posts) {
            // Display the posts
            displayPosts(posts);
        },
        error: function (error) {
            console.error('Error fetching posts:', error);
        }
    });
}

function formatDateTime(timestamp) {
    const options = { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' };
    const dateTime = new Date(timestamp).toLocaleDateString('en-US', options);
    return dateTime;
}

function displayPosts(posts) {
    var postsContainer = $('#postsContainer');

    if (posts.length > 0) {
        // Display each post
        posts.forEach(function (post) {
            var postDiv = $('<div>').addClass('news-item');

            // Display username and profile picture in one line
            var profilePicture = $('<img>').attr('src', post[7] ? post[7] : 'uploads/default.png').attr('alt', 'Profile Picture').addClass('profile-picture');
            var usernameAndPictureDiv = $('<div>').addClass('username-picture-container');
            usernameAndPictureDiv.append($('<h3>').text(`${post[5]} ${post[6]}`));
            usernameAndPictureDiv.append(profilePicture);

            // Append username and picture div
            postDiv.append(usernameAndPictureDiv);

            // Display formatted datetime with newline
            const formattedDateTime = formatDateTime(post[3]);
            postDiv.append($('<h5>').html(`${formattedDateTime}<br>`));

            // Display post content
            postDiv.append($('<p>').text(post[2]));

            // Append the post to the container
            postsContainer.append(postDiv);
        });
    } else {
        // Display a message for no posts
        postsContainer.text('No posts found.');
    }
}
