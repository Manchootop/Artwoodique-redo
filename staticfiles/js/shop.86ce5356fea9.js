document.addEventListener("DOMContentLoaded", function () {
    // Find all like buttons
    const likeButtons = document.querySelectorAll(".like-button");

    // Fetch liked status for each product on page load
    likeButtons.forEach((likeButton) => {
        const itemID = likeButton.getAttribute("data-item-id");

        // Fetch liked status for each product using a GET request
        fetch(`/get-liked-status/${itemID}/`)
            .then((response) => response.json())
            .then((data) => {
                if (data.liked) {
                    likeButton.classList.add("liked");
                    likeButton.children[0].classList.remove("far");
                    likeButton.children[0].classList.add("fa");
                }
            })
            .catch((error) => {
                console.error("Error fetching liked status:", error);
            });

        likeButton.addEventListener("click", function () {
            const itemID = likeButton.getAttribute("data-item-id");
            toggleLike(itemID, likeButton);
        });
    });

    function toggleLike(itemID, likeButton) {
        // Toggle the "like" status on the server using a POST request
        fetch("/wishlist/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ item_id: itemID }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.liked) {
                likeButton.classList.add("liked");
                likeButton.children[0].classList.remove("far");
                likeButton.children[0].classList.add("fa");
            } else {
                likeButton.classList.remove("liked");
                likeButton.children[0].classList.add("far");
                likeButton.children[0].classList.remove("fa");
            }
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
