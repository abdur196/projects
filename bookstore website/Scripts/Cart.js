export let cart= JSON.parse(localStorage.getItem('cart'));


if(!cart)
{
    cart=
    [

    ];
}

function savetostorage()
{
    localStorage.setItem('cart' , JSON.stringify(cart));
}



export function removefromcart(bookId) {
    const newcart = cart.filter((cartitem) => cartitem.bookId !== String(bookId));
    cart = newcart; 
    savetostorage(); 
    console.log("Updated cart after removal:", cart);
}


// Alternative Aproach 


//export function removefromcart(bookId) {
//     let bookIndex = -1;
    
//     for (let i = 0; i < cart.length; i++) {
//         if (cart[i].bookId === Number(bookId)) {
//             bookIndex = i;
//             break;
//         }
//     }
    
//     if (bookIndex > -1) {
//         cart.splice(bookIndex, 1);
//     }
// }
console.log(cart);