import { cart } from './Cart.js'; // We import the cart here to keep it in sync
import { sciencebooks } from './Books.js';

let booksHTML = '';

sciencebooks.forEach((book) => {
    booksHTML += `
        <div class="book-info">
            <img class="book-image" src="${book.image}" alt="Book Image">
            <div class="info">
                <p class="title">${book.title}</p>
                <p style="margin: 0;">
                    <span>by </span><span class="author"><strong>${book.author}</strong></span>
                </p>
                <p class="stats">
                    ${book.stats}
                </p>
                <p class="price">
                    $ ${book.price}
                </p>
                <span class="added" id="addedMessage">Added to Cart &#10004;</span>
                <button class="cart-button js-cart-button" data-book-id="${book.id}">
                    Add to Cart
                </button>
            </div>
        </div>
    `;
});

document.querySelector('.js-rack').innerHTML = booksHTML;

document.querySelectorAll('.js-cart-button').forEach((button) => {
    button.addEventListener('click', () => {
        const bookId = button.dataset.bookId;
        addToCart(bookId, button);
        updateCartQuantity(); // Update cart quantity after adding to cart
    });
});


function updateCartQuantity() {
    let cartQuantity = 0;
    cart.forEach((cartItem) => {
        cartQuantity += cartItem.quantity;
    });

    document.querySelector('.js-item-count').innerHTML = cartQuantity;
}


function addToCart(bookId, button) {
    let matchingBook = cart.find((item) => item.bookId === bookId);

    if (matchingBook) {
        matchingBook.quantity += 1;
    } else {
        cart.push({
            bookId: bookId,
            quantity: 1
        });
    }
    
    saveToStorage();


    const addedMessage = button.previousElementSibling;
    addedMessage.style.opacity = 1;

    setTimeout(() => {
        addedMessage.style.opacity = 0;
    }, 1000);
}


function saveToStorage() {
    localStorage.setItem('cart', JSON.stringify(cart));
}
updateCartQuantity();
