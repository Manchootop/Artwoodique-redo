from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

from .models import Order, Product, OrderItem
from ..engagements.models import WishList
from ..shared.functions import create_ref_code


@receiver(user_logged_in)
def transfer_cart_items(sender, user, request, **kwargs):
    cart = request.session.get('cart', [])
    for item_id in cart:
        item = Product.objects.get(pk=item_id)
        # Check if the item is not already in OrderItem for the user
        if not OrderItem.objects.filter(user=user, item=item).exists():
            OrderItem.objects.create(user=user, item=item, ordered=False)

    request.session['cart'] = []

user_logged_in.connect(transfer_cart_items)


@receiver(user_logged_in)
def transfer_wishlist_items(sender, user, request, **kwargs):
    wishlist = request.session.get('wishlist', [])

    # Check if a WishList instance exists for the user
    try:
        user_wishlist = WishList.objects.get(user=user)
    except WishList.DoesNotExist:
        # If no WishList instance exists, create one
        user_wishlist = WishList.objects.create(user=user)

    for item_id in wishlist:
        item = Product.objects.get(pk=item_id)

        # Check if the item is already in the user's wishlist
        if item not in user_wishlist.item.all():
            # Add the item to the user's wishlist
            user_wishlist.item.add(item)

    request.session['wishlist'] = []

user_logged_in.connect(transfer_wishlist_items)

# @receiver(user_logged_in)
# def transfer_order_items(sender, user, request, **kwargs):
#
#     order = Order.objects.filter(user=user)
#     if not order.exists():
#         Order.objects.create(user=user, ordered=False, ordered_date=timezone.now(), ref_code=create_ref_code())
#
#     if not order.ref_code:
#         order.ref_code = create_ref_code()
#         order.save()