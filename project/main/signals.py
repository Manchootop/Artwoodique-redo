from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from project.main.models import Order, Product, OrderItem


def associate_order_with_user(sender, user, request, **kwargs):
    # Check if there's an order ID stored in the session
    order_id = request.session.get('order_id')
    if order_id:
        order = Order.objects.get(id=order_id)
        order.user = user
        order.save()
        # Remove the order ID from the session
        del request.session['order_id']

user_logged_in.connect(associate_order_with_user)

@receiver(user_logged_in)
def create_order_items_for_anonymous_user(sender, user, request, **kwargs):
    if user.is_authenticated and user.username == 'anonymous':
        cart = request.session.get('cart', [])
        for item_id in cart:
            item = Product.objects.get(pk=item_id)
            OrderItem.objects.create(item=item, ordered=False)
        request.session['cart'] = []