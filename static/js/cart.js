let cart = JSON.parse(localStorage.getItem("cart")) || [];

const cartItems = document.getElementById("cartItems");
const totalPrice = document.getElementById("totalPrice");

// DISPLAY CART
function displayCart() {

    cartItems.innerHTML = "";

    let total = 0;

    cart.forEach((item, index) => {

        total += item.price;

        cartItems.innerHTML += `
            <div class="product-card">
                <h3>${item.name}</h3>
                <p>₹${item.price}</p>
                <button onclick="removeItem(${index})">
                    Remove
                </button>
            </div>
        `;
    });

    totalPrice.innerText = `Total: ₹${total}`;

    updateCartCount();
}

// REMOVE ITEM
function removeItem(index) {

    cart.splice(index, 1);

    localStorage.setItem("cart", JSON.stringify(cart));

    displayCart();
}

// UPDATE CART COUNT (NAVBAR)
function updateCartCount() {
    const cartCount = document.getElementById("cartCount");

    if (cartCount) {
        cartCount.innerText = cart.length;
    }
}

// ORDER NOW BUTTON
document.getElementById("orderNowBtn").addEventListener("click", function () {

    if (cart.length === 0) {
        alert("Cart is empty!");
        return;
    }

    alert("Order Placed Successfully 🎉");

    cart = [];

    localStorage.setItem("cart", JSON.stringify(cart));

    displayCart();
});

// INIT
displayCart();