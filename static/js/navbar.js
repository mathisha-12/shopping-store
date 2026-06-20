function updateCartCount(){

    let cart =
    JSON.parse(localStorage.getItem("cart")) || [];

    const countElement =
    document.getElementById("cartCount");

    if(countElement){
        countElement.innerText = cart.length;
    }
}

updateCartCount();