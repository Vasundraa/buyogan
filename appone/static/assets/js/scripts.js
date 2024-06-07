// static/assets/js/scripts.js

document.addEventListener("DOMContentLoaded", function () {
    var addToCartButtons = document.querySelectorAll('.cart');
    var cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];


    addToCartButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            var url = button.href;

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(response => {
                if (response.ok) {
                    return response.json();
                }
                return response.text().then(text => {
                    throw new Error('Network response was not ok: ' + text);
                });
            }).then(data => {
                if (data.success) {
                    // Update cart UI here with data.product, data.quantity, data.total_price
                    console.log('Product added to cart:', data.product);
                    // Add the product to the cart side menu
                    updateCartSideMenu(data.product, data.quantity);
                    // Update the total price in the cart UI
                    document.getElementById('cart-total').textContent = data.total_price.toFixed(2);
                    // Store cart items in localStorage
                    var newItem = { product: data.product, quantity: data.quantity };
                    cartItems.push(newItem);
                    localStorage.setItem('cartItems', JSON.stringify(cartItems));
                }
            }).catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    });

    function updateCartSideMenu(product, quantity) {
        var cartItemsContainer = document.getElementById('cart-items-container');
        var cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <p>${product}</p>
            <p>Quantity: ${quantity}</p>
        `;
        cartItemsContainer.appendChild(cartItem);
    }

    // Function to initialize cart from localStorage
    function initializeCartFromStorage() {
        cartItems.forEach(item => {
            updateCartSideMenu(item.product, item.quantity);
        });
    }

    initializeCartFromStorage();
});