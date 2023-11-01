document.addEventListener("DOMContentLoaded", function () {
    // Find all like buttons
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach((likeButton) => {
        likeButton.addEventListener("click", function () {
            const itemID = likeButton.getAttribute("data-item-id"); // Get the item ID from the data attribute
            console.log(itemID);
            toggleLike(itemID, likeButton);
        });
    });

    function toggleLike(itemID, likeButton) {
        console.log(itemID);

        // Toggle the "like" status on the server
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
