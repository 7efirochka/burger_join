document.addEventListener('DOMContentLoaded', function() {
    // Cart UI elements
    const cartContainer = document.getElementById('cart-container');
    const cartPreview = document.getElementById('cart-preview');
    const cartItemsContainer = document.getElementById('cart-preview-items');
    const cartTotalElement = document.getElementById('cart-total');
    const cartCountElement = document.getElementById('cart-count');
    const openCartButton = document.getElementById('open-cart-button');
    const closeCartButton = document.getElementById('close-cart-button');
    
    // Login modal for unauthorized users
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'), {
        keyboard: false
    });

    // Show/hide cart
    if (openCartButton) {
        openCartButton.addEventListener('click', function() {
            cartPreview.classList.add('show');
        });
    }
    
    if (closeCartButton) {
        closeCartButton.addEventListener('click', function() {
            cartPreview.classList.remove('show');
        });
    }

    // Add to cart handlers
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const productId = this.dataset.productId;
            const productType = this.dataset.productType || 'burgers';
            
            try {
                const response = await fetch('/menu/cart/add/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        product_id: productId,
                        product_type: productType
                    })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    // Update cart count
                    if (cartCountElement) {
                        cartCountElement.textContent = data.cart_count;
                    }
                    
                    // Show success message
                    showToast('Товар добавлен в корзину', 'success');
                    
                    // Open cart preview
                    if (cartPreview) {
                        cartPreview.classList.add('show');
                        
                        // Refresh cart items
                        refreshCartItems();
                    }
                } else if (data.status === 'error' && data.redirect) {
                    // Show login modal for unauthorized users
                    loginModal.show();
                } else {
                    showToast(data.message || 'Произошла ошибка', 'error');
                }
            } catch (error) {
                console.error('Error adding to cart:', error);
                showToast('Произошла ошибка при добавлении товара', 'error');
            }
        });
    });

    // Cart item quantity change handlers
    document.addEventListener('click', function(e) {
        // Increase quantity
        if (e.target.classList.contains('cart-item-increase')) {
            const itemId = e.target.dataset.cartItemId;
            changeCartItemQuantity(itemId, 'increase');
        }
        
        // Decrease quantity
        if (e.target.classList.contains('cart-item-decrease')) {
            const itemId = e.target.dataset.cartItemId;
            changeCartItemQuantity(itemId, 'decrease');
        }
        
        // Remove item
        if (e.target.classList.contains('cart-item-remove')) {
            const itemId = e.target.dataset.cartItemId;
            removeCartItem(itemId);
        }
    });

    // Helper function to change cart item quantity
    async function changeCartItemQuantity(itemId, action) {
        try {
            const response = await fetch('/menu/cart/change/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    cart_item_id: itemId,
                    action: action
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                if (data.removed) {
                    // Item was removed (quantity became 0)
                    const itemElement = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
                    if (itemElement) {
                        itemElement.remove();
                    }
                } else {
                    // Update quantity display
                    const quantityInput = document.querySelector(`.cart-item[data-item-id="${itemId}"] input.number`);
                    if (quantityInput) {
                        quantityInput.value = data.item_quantity;
                    }
                    
                    // Update item total
                    const itemTotal = document.querySelector(`.cart-item[data-item-id="${itemId}"] .item-total`);
                    if (itemTotal) {
                        itemTotal.textContent = data.item_total + ' ₽';
                    }
                }
                
                // Update cart count
                if (cartCountElement) {
                    cartCountElement.textContent = data.cart_count;
                }
                
                // Update cart total
                if (cartTotalElement) {
                    cartTotalElement.textContent = data.cart_total;
                }
                
                // If cart is empty, refresh to show empty state
                if (data.cart_count === 0) {
                    refreshCartItems();
                }
            } else if (data.status === 'error' && data.redirect) {
                loginModal.show();
            } else {
                showToast(data.message || 'Произошла ошибка', 'error');
            }
        } catch (error) {
            console.error('Error changing quantity:', error);
            showToast('Произошла ошибка при изменении количества', 'error');
        }
    }

    // Helper function to remove cart item
    async function removeCartItem(itemId) {
        try {
            const response = await fetch('/menu/cart/remove/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    cart_item_id: itemId
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Remove item from DOM
                const itemElement = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
                if (itemElement) {
                    itemElement.remove();
                }
                
                // Update cart count
                if (cartCountElement) {
                    cartCountElement.textContent = data.cart_count;
                }
                
                // Update cart total
                if (cartTotalElement) {
                    cartTotalElement.textContent = data.cart_total;
                }
                
                // If cart is empty, refresh to show empty state
                if (data.cart_count === 0) {
                    refreshCartItems();
                }
                
                showToast('Товар удален из корзины', 'success');
            } else if (data.status === 'error' && data.redirect) {
                loginModal.show();
            } else {
                showToast(data.message || 'Произошла ошибка', 'error');
            }
        } catch (error) {
            console.error('Error removing item:', error);
            showToast('Произошла ошибка при удалении товара', 'error');
        }
    }

    // Helper function to refresh cart items
    function refreshCartItems() {
        location.reload(); // Simple approach - could be replaced with AJAX
    }

    // Helper function to show toast notifications
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            // Create toast container if it doesn't exist
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const toastElement = document.createElement('div');
        toastElement.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type}`;
        toastElement.id = toastId;
        toastElement.setAttribute('role', 'alert');
        toastElement.setAttribute('aria-live', 'assertive');
        toastElement.setAttribute('aria-atomic', 'true');
        
        toastElement.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        document.getElementById('toast-container').appendChild(toastElement);
        
        const toast = new bootstrap.Toast(toastElement, {
            delay: 3000
        });
        toast.show();
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


//document.addEventListener('DOMContentLoaded', () => {
//  const btn = document.createElement('button');
//  btn.id = 'cartToggleBtn';
//  btn.className = 'floating-cart-btn';
//  btn.innerHTML = '<i class="fas fa-shopping-cart"></i><span class="cart-badge">0</span>';
//  document.body.appendChild(btn);
//});