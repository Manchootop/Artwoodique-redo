// Get the current URL or page name
const currentPage = window.location.pathname;

// Find the corresponding breadcrumb link and highlight it
document.querySelectorAll('.breadcrumbs a').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
        link.classList.add('current-page');
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const likeButton = document.querySelector(".like-button");
    let isLiked = false;

    likeButton.addEventListener("click", function () {
        if (isLiked) {
            // Handle the case when the button is already liked
            toggleLike(false); // Call a function to toggle the like state and send an AJAX request
        } else {
            // Handle the case when the button is not liked
            toggleLike(true); // Call a function to toggle the like state and send an AJAX request
        }
    });

    function toggleLike(like) {
        // Send an AJAX request to like/unlike the item on the server
        fetch("/like", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ item_id: 123, liked: like }), // Send item ID and liked status
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.liked) {
                    // Item is liked, update the UI
                    likeButton.classList.add("liked");
                } else {
                    // Item is unliked, update the UI
                    likeButton.classList.remove("liked");
                }
                isLiked = data.liked; // Update the liked state
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(";").shift();
    }
});
