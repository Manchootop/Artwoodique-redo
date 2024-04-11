from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from project.main.models import OrderItem, Product, Order


def add_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # If the user is authenticated, add the product to their cart in the database
    if request.user.is_authenticated:
        order_item, created = OrderItem.objects.get_or_create(user=request.user, item=product)
        if created:
            messages.success(request, 'This item was added to your cart.')
        else:
            messages.info(request, 'This item is already in your cart.')

    # If the user is not authenticated, add the product to their cart in the session
    else:
        cart = request.session.get('cart', [])
        request.session.save()
        if product.pk in cart:
            messages.info(request, 'This item is already in your cart.')
        else:
            cart.append(product.pk)
            request.session['cart'] = cart
            request.session.save()
            messages.success(request, 'This item was added to your cart.')

    return redirect('store')
