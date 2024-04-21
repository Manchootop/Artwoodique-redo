// JavaScript code for rendering products grouped by attributes
const btn = document.getElementById('submit');
btn.addEventListener('click', function (event) {
    // Get the value of the title input
    const titleValue = document.getElementById('title').value.trim();

    // Check if the title is empty
    if (titleValue === '') {
        // Prevent form submission
        event.preventDefault();

        // Display an error message
        const errorMessage = document.createElement('p');
        errorMessage.textContent = 'Title cannot be empty.';
        errorMessage.style.color = 'red';

        // Append error message to the form
        const errorDiv = document.querySelector(".error-msg");
        errorDiv.appendChild(errorMessage);

        // Set a timeout to remove the error message after a few seconds
        setTimeout(function () {
            errorMessage.remove();
        }, 3000); // Remove error message after 3 seconds
    }
});



const button = document.querySelector('.actions input');
button.addEventListener('click', function (event) {
    event.preventDefault();

    const attributes = {
        material: document.querySelector('#material').value,
        size: document.querySelector('#size').value,
        type: document.querySelector('#type').value,
        title: document.querySelector('#title').value, // Include the title in the attributes object

    };
    fetchSimilarProducts(attributes);
});

// Function to fetch similar products based on attributes
function fetchSimilarProducts(attributes) {
    const url = '/designer/';
    const queryParams = new URLSearchParams(attributes).toString();
    const csrftoken = getCookie('csrftoken');
    console.log(queryParams, url, attributes);
    const spinnerContainer = document.querySelector('.spinner-container');
    spinnerContainer.style.display = 'block';


    fetch(`${url}?${queryParams}`, {
        method: 'POST', // Specify the request method
        headers: {
            'Content-Type': 'application/json', // Specify the content type
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(attributes) // Serialize the attributes object
    })
        .then(response => response.json())
        .then(data => {
            // Simulate 2-second delay before hiding the spinner
            setTimeout(() => {
                // Hide spinner after delay
                spinnerContainer.style.display = 'none';
                // Render sections based on grouped products
                renderSections(data);
            }, 2000); // 2-second delay
        })
        .catch(error => {
            console.error('Error fetching similar products:', error);
            // Hide spinner in case of error
            spinnerContainer.style.display = 'none';
        });
}

// Function to render sections based on grouped products
function renderSections(groupedProducts) {
        // Clear sections before rendering new products
    const sections = document.querySelectorAll('.cards');
    sections.forEach(section => {
        section.innerHTML = ''; // Remove all content inside the section
    });

    for (const attribute in groupedProducts) {
        if (groupedProducts.hasOwnProperty(attribute)) {
            if (attribute === 'title') {
                return;
            }
            const sectionId = `${attribute.toLowerCase()}`;
            const section = document.getElementById(sectionId);
            console.log(sectionId, "ALABALA");
            if (section) {
                // If the section exists, update its <h2> tag
                const heading = section.querySelector('h2');
                if (heading) {
                    heading.textContent = `Similar ${attribute}`;
                }

                // Render products for the specified attribute
                renderProducts(groupedProducts[attribute], sectionId);
            }
        }
    }
}


// Function to render products for the specified attribute
function renderProducts(products, attribute) {
    if (attribute === 'title') {
        return;
    }
    console.log(products, "alabala");
    const section = document.getElementById(`${attribute}`);
    // use func create section
    if (products.length === 0) {
        section.innerHTML += '<p>No products found.</p>';
    } else {
        products.forEach(product => {
            const card = createCard(product);
            section.appendChild(card);
        });

    }
}


function createCard(product) {
    const card = document.createElement('div');
    card.classList.add('card');

    if (product.discount_price !== 0.0) {
        const cardBadges = document.createElement('div');
        cardBadges.classList.add('card-badges');

        const discountBadge = document.createElement('div');
        discountBadge.classList.add('card-badge', 'badge--discount');
        discountBadge.innerHTML = `<span class="badge-label">-${product.discount_price} лв.</span>`;
        cardBadges.appendChild(discountBadge);

        card.appendChild(cardBadges);
    }
    //
    // const likeButton = document.createElement('a');
    // likeButton.classList.add('like-button');
    // likeButton.href = `/add-to-wishlist/${product.id}`;
    // likeButton.setAttribute('data-item-id', product.id);
    // likeButton.style.textDecoration = 'none';
    // likeButton.innerHTML = '<i class="far fa-heart"></i>';
    // card.appendChild(likeButton);

    const productLink = document.createElement('a');
    productLink.href = `/details/${product.id}`;
    const productImage = document.createElement('img');
    productImage.classList.add('product-image')
    productImage.src = product.image;
    productImage.alt = 'product_image';
    productLink.appendChild(productImage);
    card.appendChild(productLink);

    const cardDetails = document.createElement('div');
    cardDetails.classList.add('card-details');

    const productTitle = document.createElement('a');
    productTitle.classList.add('product-title');
    productTitle.href = `/details/${product.id}`;
    productTitle.style.display = '-webkit-box';
    productTitle.style.maxWidth = '20ch';
    productTitle.style.webkitLineClamp = '2';
    productTitle.textContent = product.title;
    cardDetails.appendChild(productTitle);

    const cardContent = document.createElement('div');
    cardContent.classList.add('card-content');

    const cardPricing = document.createElement('div');
    cardPricing.classList.add('card-pricing');

    if (product.discount_price) {
        const cardPriceOld = document.createElement('div');
        cardPriceOld.classList.add('card-price-old');
        cardPriceOld.innerHTML = `<s><span>${product.price}лв.</span></s>`;
        cardPricing.appendChild(cardPriceOld);
    }

    const cardPriceCurrent = document.createElement('div');
    cardPriceCurrent.classList.add('card-price-current');
    cardPriceCurrent.innerHTML = `<span>${product.price}лв.</span>`;

    cardContent.appendChild(cardPricing);

    const cardBuy = document.createElement('div');
    cardBuy.classList.add('card-price-current');
    cardBuy.appendChild(cardPriceCurrent);

    const buyButton = document.createElement('a');
    buyButton.href = `/orders/add-to-cart/${product.slug}`;
    buyButton.classList.add('btn');
    buyButton.setAttribute('aria-label', 'Product details');
    const iElement = document.createElement('i');
    iElement.classList.add('em', 'em-cart_fill',);

    // buyButton.innerHTML = `<i class="em em-cart_fill"></i>`;
    const img = document.createElement('img');
    img.classList.add('cart-icon');
    img.src = '/static/images/cart.svg'

    iElement.appendChild(img);
    buyButton.appendChild(iElement);

    cardBuy.appendChild(buyButton);

    cardContent.appendChild(cardBuy);

    cardDetails.appendChild(cardContent);

    card.appendChild(cardDetails);

    return card;
}


// Example: Fetch similar products when the page loads
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if cookie name matches the specified name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Extract and decode the CSRF token
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

