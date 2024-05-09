function onSortOptionChange() {
    var selectElement = document.getElementById('sort-select');
    console.log('Sort option changed to:', selectElement.value);
    document.getElementById('sort-form').submit();
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// // JavaScript code to update the cart count dynamically
// function updateCartCount() {
//     $.ajax({
//         url: '/orders/context_processors.py/cart_items_count/', // URL of the endpoint created in step 1
//         success: function(response) {
//             // Update the cart count in the UI
//             $('.cart-items-count').text(response.cart_items_count);
//         },
//         error: function(xhr, status, error) {
//             console.error('Error fetching cart count:', error);
//         }
//     });
// }

// $(document).ready(function() {
//     // Handle click event on both specified tags
//     $("a.cart").click(function(e) {
//         e.preventDefault(); // Prevent the default action of following the link

//         // Extract product ID from the value attribute
//         var productId = $(this).attr("value");

//         // Make an AJAX request to add the product to the cart
//         $.ajax({
//             type: "POST",
//             url: "/orders/addtocart/",  // URL to your backend view for adding to the cart
//             data: {
//                 product_id: productId
//             },
//             success: function(response) {
//                 // Handle success response (maybe update the cart icon or show a message)
//                 alert("Product added to cart successfully!");
//             },
//             error: function(xhr, textStatus, errorThrown) {
//                 // Handle error response
//                 alert("Error adding product to cart. Please try again later.");
//             }
//         });
//     });
//     updateCartCount();
// });


$(document).ready(function() {
    // Function to update the cart count dynamically
    function updateCartCount() {
        $.ajax({
            url: '/orders/context_processors.py/cart_items_count/', // URL to your view that returns the cart count
            success: function(response) {
                // Update the cart count in the UI
                $('.cart-items-count').text(response.cart_items_count);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching cart count:', error);
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        const quantityInputs = document.querySelectorAll('.quantity-box input');
        
        quantityInputs.forEach(function(input) {
            input.addEventListener('input', function() {
                const quantity = parseInt(input.value);
                const price = parseFloat(input.dataset.price);
                const totalPriceElement = input.parentElement.nextElementSibling.querySelector('.total-price');
                const newTotalPrice = price * quantity;
                totalPriceElement.textContent = '$' + newTotalPrice.toFixed(2);
            });
        });
    });
    // Handle click event on cart button to add product to cart
    $("a.cart").click(function(e) {
        e.preventDefault(); // Prevent the default action of following the link

        // Extract product ID from the value attribute
        var productId = $(this).attr("value");

        // Make an AJAX request to add the product to the cart
        $.ajax({
            type: "POST",
            url: "/orders/addtocart/",  // URL to your backend view for adding to the cart
            data: {
                product_id: productId
            },
            success: function(response) {
                // Handle success response (maybe update the cart icon or show a message)
                alert("Product added to cart successfully!");

                // Update cart count dynamically after successful addition
                updateCartCount();
            },
            error: function(xhr, textStatus, errorThrown) {
                // Handle error response
                alert("Error adding product to cart. Please try again later.");
            }
        });
    });

    // Call updateCartCount function initially when the page loads
    updateCartCount();  // Update cart count when the page loads

    // Optionally, you can set a timer to update the cart count periodically
    // setInterval(updateCartCount, 5000);  // Update cart count every 5 seconds (for example)
});






// $(document).ready(function() {
//     // Handle click event on delete cart item button
//     $(".delete-cart-item").click(function(e) {
//         e.preventDefault(); // Prevent the default action of following the link

//         // Extract cart item ID from data attribute
//         var cartItemId = $(this).data("cart-item-id");

//         // Make an AJAX request to delete the cart item
//         $.ajax({
//             type: "POST",
//             url: "/orders/cart/delete/" + cartItemId + "/",  // URL to your backend view for deleting cart items
//             success: function(response) {
//                 // Reload the page after successful deletion
//                 location.reload();
//             },
//             error: function(xhr, textStatus, errorThrown) {
//                 // Handle error response
//                 console.error('Error deleting cart item:', errorThrown);
//             }
//         });
//     });
// });



