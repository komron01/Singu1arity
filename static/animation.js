document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        // Select elements by class name
        var leftContainer = document.querySelector(".left-image-container");
        var rightContainer = document.querySelector(".right-image-container");

        // Adding classes for animation
        leftContainer.classList.add("move-left");
        rightContainer.classList.add("move-right");

        // Set a timer to remove elements after the animation duration
        setTimeout(function () {
            // Remove elements
            leftContainer.remove();
            rightContainer.remove();

            // Restore pointer events
            document.querySelectorAll('.profile-info *').forEach(function (el) {
                el.style.pointerEvents = 'auto';
            });
            document.querySelectorAll('.friends-list *').forEach(function (el) {
                el.style.pointerEvents = 'auto';
            });
            document.querySelectorAll('.news-feed *').forEach(function (el) {
                el.style.pointerEvents = 'auto';
            });
        }, 2000); // Adjust the duration based on your animation duration
    }, 2000); // Adjust the timing based on your requirements

    // Block pointer events during animation
    document.querySelectorAll('.profile-info *').forEach(function (el) {
        el.style.pointerEvents = 'none';
    });
    document.querySelectorAll('.friends-list *').forEach(function (el) {
        el.style.pointerEvents = 'none';
    });
    document.querySelectorAll('.news-feed *').forEach(function (el) {
        el.style.pointerEvents = 'none';
    });
});
