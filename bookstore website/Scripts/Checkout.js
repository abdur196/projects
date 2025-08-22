import { cart, removefromcart } from './Cart.js';
import { books } from './Books.js';

let cartsummaryHTML = '';
let subtotal = 0;
const shippingCost = 4.99; // Fixed shipping cost
const taxRate = 0.10; // Tax rate
const today = dayjs();
const threeday = today.add(3, 'days');
const threedaydelivery = threeday.format('dddd, MMMM D');

// Build the cart summary
cart.forEach((cartitem) => {
  const bookId = Number(cartitem.bookId);
  let matchingbook;

  books.forEach((book) => {
    if (book.id === bookId) {
      matchingbook = book;
    }
  });

  if (!matchingbook) return;

  const itemTotalPrice = Number(matchingbook.price) * cartitem.quantity;
  subtotal += itemTotalPrice;

  cartsummaryHTML += `
    <div class="cart-item-container js-cart-item-container-${matchingbook.id}">
      <div class="cart-item-details-grid">
        <img class="product-image" src="${matchingbook.image}">
        <div class="cart-item-details">
          <div class="product-name">${matchingbook.title}</div>
          <div class="product-price">$${Number(matchingbook.price).toFixed(2)}</div>
          <div class="product-quantity">
            <input type="number" class="quantity-input" value="${cartitem.quantity}" min="1">
            <span class="update-quantity-link" data-book-id="${matchingbook.id}">Update</span>
            <span class="delete-quantity-link js-delete-book" data-book-id="${matchingbook.id}">Delete</span>
          </div>
          <div class="delivery-date">${threedaydelivery}</div>
        </div>
      </div>
    </div>
  `;
});

document.querySelector('.js-cart-summary').innerHTML = cartsummaryHTML;

const tax = subtotal * taxRate;
const total = subtotal + shippingCost + tax;

document.querySelector('.items-count').textContent = cart.length;
document.querySelector('.items-total').textContent = `$${subtotal.toFixed(2)}`;
document.querySelector('.shipping-total').textContent = `$${shippingCost.toFixed(2)}`;
document.querySelector('.subtotal-total').textContent = `$${(subtotal + shippingCost).toFixed(2)}`;
document.querySelector('.tax-total').textContent = `$${tax.toFixed(2)}`;
document.querySelector('.order-total').textContent = `$${total.toFixed(2)}`;

// Event listener for delete book
document.querySelectorAll('.js-delete-book').forEach((link) => {
  link.addEventListener('click', () => {
    const bookId = link.dataset.bookId;
    removefromcart(bookId);

    const container = document.querySelector(`.js-cart-item-container-${bookId}`);
    container.remove();

    recalculateOrderSummary();
  });
});

// Event listener for update quantity
document.querySelectorAll('.update-quantity-link').forEach((link) => {
  link.addEventListener('click', () => {
    const bookId = link.dataset.bookId;
    const quantityInput = link.previousElementSibling; // Get the input element
    const newQuantity = Number(quantityInput.value);

    // Update the cart with the new quantity
    const cartItemIndex = cart.findIndex(item => item.bookId === bookId);
    if (cartItemIndex !== -1) {
      cart[cartItemIndex].quantity = newQuantity;
    }

    recalculateOrderSummary();
  });
});

// Function to recalculate the order summary
function recalculateOrderSummary() {
  subtotal = 0;

  cart.forEach((cartitem) => {
    const bookId = Number(cartitem.bookId);
    let matchingbook;

    books.forEach((book) => {
      if (book.id === bookId) {
        matchingbook = book;
      }
    });

    if (!matchingbook) return;

    const itemTotalPrice = Number(matchingbook.price) * cartitem.quantity;
    subtotal += itemTotalPrice;
  });

  const tax = subtotal * taxRate;
  const total = subtotal + shippingCost + tax;

  document.querySelector('.items-count').textContent = cart.length;
  document.querySelector('.items-total').textContent = `$${subtotal.toFixed(2)}`;
  document.querySelector('.shipping-total').textContent = `$${shippingCost.toFixed(2)}`;
  document.querySelector('.subtotal-total').textContent = `$${(subtotal + shippingCost).toFixed(2)}`;
  document.querySelector('.tax-total').textContent = `$${tax.toFixed(2)}`;
  document.querySelector('.order-total').textContent = `$${total.toFixed(2)}`;
}
