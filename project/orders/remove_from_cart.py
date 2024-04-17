from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from project.main.models import Product
from project.orders.models import OrderItem


def remove_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # If the user is authenticated, remove the product from their cart in the database
    if request.user.is_authenticated:
        print(f'Removing {product} with id: {product.id} from {request.user}')
        order_item = OrderItem.objects.filter(user=request.user, item=product)
        if order_item.exists():
            order_item.delete()
            messages.success(request, 'This item was removed from your cart.')
        else:
            messages.info(request, 'This item is not in your cart.')

    # If the user is not authenticated, remove the product from their cart in the session
    else:
        cart = request.session.get('cart', [])
        if product.pk in cart:
            cart.remove(product.pk)
            request.session['cart'] = cart
            request.session.save()
            messages.success(request, 'This item was removed from your cart.')
        else:
            messages.info(request, 'This item is not in your cart.')

    return redirect('cart')