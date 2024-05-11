document.addEventListener("DOMContentLoaded", function () {
    const contactLink = document.getElementById("contactLink");
    const popup = document.getElementById("popup");
    const closePopup = document.getElementById("closePopup");

    contactLink.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default link behavior
        popup.style.display = "block";
    });

    closePopup.addEventListener("click", function () {
        popup.style.display = "none";
    });

    // Get all the sidebar images
    const sidebarImages = document.querySelectorAll('.down-row img');

    // Get the main image element
    const mainImage = document.querySelector('.up-row img');

    // Get the left and right arrow elements
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
    console.log(sidebarImages)

    // Initialize the current image index
    let currentImageIndex = 0;

    // Function to update the main image and active class
    function updateMainImage() {
        // Remove the 'active' class from all sidebar images
        sidebarImages.forEach((img) => {
            img.classList.remove('active');
        });

        // Add the 'active' class to the current image
        sidebarImages[currentImageIndex].classList.add('active');

        // Set the main image's src to the current image's src
        mainImage.src = sidebarImages[currentImageIndex].src;
    }

    // Function to handle click on sidebar images
    function handleSidebarImageClick(index) {
        currentImageIndex = index;
        updateMainImage();
    }

    // Function to handle touch on sidebar images
    function handleSidebarImageTouch(index) {
        currentImageIndex = index;
        updateMainImage();
    }

    // Event listener for the right arrow
    if (rightArrow) {
        rightArrow.addEventListener('click', () => {
            incrementImageIndex();
        });
    }

    // Event listener for the left arrow
    if (leftArrow) {
        leftArrow.addEventListener('click', () => {
            decrementImageIndex();
        });
    }

    // Add click event listener to each sidebar image
    sidebarImages.forEach((image, index) => {
        image.addEventListener('click', () => {
            handleSidebarImageClick(index);
        });

        // Add touch event listener to each sidebar image
        image.addEventListener('touchstart', (event) => {
            event.preventDefault(); // Prevent the default touch behavior
            handleSidebarImageTouch(index);
        });
        image.addEventListener('touchend', (event) => {
            event.preventDefault(); // Prevent the default touch behavior
        });
    });

    // Initialize the main image
    updateMainImage();

    // Function to increment the current image index
    function incrementImageIndex() {
        currentImageIndex++;

        // Check if it exceeds the number of images, and loop back to the beginning if needed
        if (currentImageIndex >= sidebarImages.length) {
            currentImageIndex = 0;
        }

        // Update the main image
        updateMainImage();
    }

    // Function to decrement the current image index
    function decrementImageIndex() {
        currentImageIndex--;

        // Check if it goes below zero, and loop to the end if needed
        if (currentImageIndex < 0) {
            currentImageIndex = sidebarImages.length - 1;
        }

        // Update the main image
        updateMainImage();
    }
});
