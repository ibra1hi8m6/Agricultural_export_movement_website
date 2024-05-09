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


let btns = document.querySelectorAll(".product-categorie-box a.cart")
btns.forEach(btn=>{
btn.addEventListener("click", addToCart)
})
function addToCart(e) {
e.preventDefault();
let product_id = e.target.getAttribute('value');
console.log(product_id);
// Now you have the product ID, you can proceed with adding the product to the cart

let url = "/orders/addtocart"

let data = {id:product_id}

fetch(url, {
method: "POST",
headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
body: JSON.stringify(data)
})
.then(res=>res.json())
.then(data=>{
document.getElementById("num_of_items").innerHTML = data
console.log(data)
})
.catch(error=>{
console.log(error)
})
}
