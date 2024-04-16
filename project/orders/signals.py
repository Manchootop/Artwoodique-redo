from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

from .models import Order, Product, OrderItem
from ..engagements.models import WishList


# def associate_order_with_user(sender, user, request, **kwargs):
#     # Check if there's an order ID stored in the session
#     order_id = request.session.get('order_id')
#     if order_id:
#         order = Order.objects.get(id=order_id)
#         order.user = user
#         order.save()
#         # Remove the order ID from the session
#         del request.session['order_id']
#
#
# user_logged_in.connect(associate_order_with_user)
#

# @receiver(user_logged_in)
# def create_order_items_for_anonymous_user(sender, user, request, **kwargs):
#     cart = request.session.get('cart', [])
#     if user.is_authenticated:
#         for item_id in cart:
#             item = Product.objects.get(pk=item_id)
#             # Check if the item is not already in OrderItem for the user
#             if not OrderItem.objects.filter(user=user, item=item).exists():
#                 OrderItem.objects.create(user=user, item=item, ordered=False)
#         request.session['cart'] = []

# @receiver(post_save, sender=UserModel)
# def create_order_items_for_anonymous_user(sender, user, request, **kwargs):
#     print('triggered')
#     cart = request.session.get('cart', [])
#     if user.is_authenticated:
#         for item_id in cart:
#             item = Product.objects.get(pk=item_id)
#             # Check if the item is not already in OrderItem for the user
#             if not OrderItem.objects.filter(user=user, item=item).exists():
#                 OrderItem.objects.create(user=user, item=item, ordered=False)
#         request.session['cart'] = []
#     else:
#         # If the user is not authenticated, associate items with a temporary user ID
#         temp_user_id = request.session.get('temp_user_id')
#         if not temp_user_id:
#             temp_user_id = str(uuid.uuid4())  # Generate a unique temporary user ID
#             request.session['temp_user_id'] = temp_user_id
#
#         for item_id in cart:
#             item = Product.objects.get(pk=item_id)
#             # Check if the item is not already in OrderItem for the temporary user
#             if not OrderItem.objects.filter(temp_user_id=temp_user_id, item=item).exists():
#                 OrderItem.objects.create(temp_user_id=temp_user_id, item=item, ordered=False)
#         request.session['cart'] = []

@receiver(user_logged_in)
def transfer_cart_items(sender, user, request, **kwargs):
    cart = request.session.get('cart', [])

    for item_id in cart:
        order_item, created = OrderItem.objects.get_or_create(user=user, item__id=item_id)
        item = Product.objects.get(pk=item_id)
        # Check if the item is not already in OrderItem for the user
        if not order_item.exists():
            OrderItem.objects.create(user=user, item=item, ordered=False)

    request.session['cart'] = []

user_logged_in.connect(transfer_cart_items)


@receiver(user_logged_in)
def transfer_wishlist_items(sender, user, request, **kwargs):

    cart = request.session.get('cart', [])
    print('alabala')
    for item_id in cart:
        item = Product.objects.get(pk=item_id)
        wishlist = WishList.objects.filter(user=user, item__id=item_id)
        if not wishlist.exists():
            WishList.objects.create(user=user, item=item)
    request.session['cart'] = []

user_logged_in.connect(transfer_cart_items)