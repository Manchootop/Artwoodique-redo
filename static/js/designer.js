// JavaScript code for rendering products grouped by attributes
const button = document.querySelector('.actions input');
button.addEventListener('click', function(event) {
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
    const url = '/orders/';
    const queryParams = new URLSearchParams(attributes).toString();
    const csrftoken = getCookie('csrftoken');
    console.log(queryParams, url, attributes);
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
        // Render sections based on grouped products
        renderSections(data);
    })
    .catch(error => {
        console.error('Error fetching similar products:', error);
    });
}

// Function to render sections based on grouped products
function renderSections(groupedProducts) {
    for (const attribute in groupedProducts) {
        if (groupedProducts.hasOwnProperty(attribute)) {
            renderProducts(groupedProducts[attribute], attribute);
        }
    }
}

// Function to render products for the specified attribute
function renderProducts(products, attribute) {
    if (attribute === 'title') {
        return;
    }
    const section = document.getElementById(`${attribute}`);
    console.log(section);
    console.log(attribute);
    section.innerHTML = `<h2>${attribute.charAt(0).toUpperCase() + attribute.slice(1)} Products</h2>`;

    if (products.length === 0) {
        section.innerHTML += '<p>No products found.</p>';
    } else {
        const productList = document.createElement('ul');
        products.forEach(product => {
            const listItem = document.createElement('li');
            listItem.textContent = product.price; // Assuming 'title' is the product attribute to display
            productList.appendChild(listItem);
        });
        section.appendChild(productList);
    }
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