from Orders.models import CartItem

def cart_items_count(request):
    # Calculate the count of cart items for the current user
    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        cart_items_count = 0  # If the user is not authenticated, set count to 0

    # Return the count as a dictionary
    return {'cart_items_count': cart_items_count}
# from django.http import JsonResponse
# from .models import CartItem

# def cart_items_count(request):
#     if request.user.is_authenticated:
#         cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
#     else:
#         cart_items_count = 0
#     return JsonResponse({'cart_items_count': cart_items_count})