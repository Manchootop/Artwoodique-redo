// Get all the sidebar images
const sidebarImages = document.querySelectorAll('.down-row img');

// Get the main image element
const mainImage = document.querySelector('.up-row img');

// Get the left and right arrow elements
const leftArrow = document.querySelector('.left-arrow');
const rightArrow = document.querySelector('.right-arrow');

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

// Event listener for the right arrow
rightArrow.addEventListener('click', () => {
    // Increment the current image index
    currentImageIndex++;

    // Check if it exceeds the number of images, and loop back to the beginning if needed
    if (currentImageIndex >= sidebarImages.length) {
        currentImageIndex = 0;
    }

    // Update the main image
    updateMainImage();
});

// Event listener for the left arrow
leftArrow.addEventListener('click', () => {
    // Decrement the current image index
    currentImageIndex--;

    // Check if it goes below zero, and loop to the end if needed
    if (currentImageIndex < 0) {
        currentImageIndex = sidebarImages.length - 1;
    }

    // Update the main image
    updateMainImage();
});

// Add a click event listener to each sidebar image
sidebarImages.forEach((image, index) => {
    image.addEventListener('click', () => {
        // Handle click on sidebar image
        handleSidebarImageClick(index);
    });
});

// Initial update of the main image
updateMainImage();


// Add your JavaScript here



