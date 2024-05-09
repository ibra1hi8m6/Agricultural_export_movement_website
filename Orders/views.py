from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import Products
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@login_required
def CartPage(request):
    # Retrieve cart items for the current user
    cart_items = CartItem.objects.filter(cart__user=request.user)
# Calculate cart items count
    cart_items_count = cart_items.count()

    return render(request, 'Orders_html/cart.html', {'cart_items': cart_items, 'cart_items_count': cart_items_count})



@login_required
def delete_cart_item(request, cart_item_id):
    # Retrieve the cart item
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)

    # Check if the cart item belongs to the current user
    if cart_item.cart.user != request.user:
        return JsonResponse({'error': 'You are not authorized to delete this item'}, status=403)

    # Delete the cart item
    cart_item.delete()

    # Redirect back to the cart page after deletion
    cart_items = CartItem.objects.filter(cart__user=request.user)
# Calculate cart items count
    cart_items_count = cart_items.count()

    return render(request, 'Orders_html/cart.html', {'cart_items': cart_items, 'cart_items_count': cart_items_count})

def CheckoutPage(request):
    
    return render(request, 'Orders_html/checkout.html')





@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        # Fetch the product using the product_id
        # Assuming you have a function to get the product object by ID
        product = Product.objects.get(id=product_id)

        # Assuming you have a function to get or create the cart for the current user
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

        # Add the product to the cart or update its quantity if already added
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 10
        cart_item.save()

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})





@login_required
def create_order(request):
    if request.method == 'POST':
        cart = CartItem.objects.get(user=request.user, completed=False)
        order = Order.objects.create(user=request.user)
        for item in cart.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.completed = True  # Mark the cart as completed
        cart.save()
        return JsonResponse({'success': 'Order created successfully', 'order_id': order.id})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def manage_orders(request):
    if not request.user.is_exporter:  # Assume there's a way to identify exporter users
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    orders = Order.objects.filter(status='Pending')
    return render(request, 'manage_orders.html', {'orders': orders})




@login_required
def update_order_status(request, order_id, status):
    if not request.user.is_exporter:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    order = Order.objects.get(id=order_id)
    order.status = status
    order.save()
    return JsonResponse({'success': f'Order status updated to {status}'})