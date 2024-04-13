from django import template


register = template.Library()


@register.filter
def cart_item_count(request):
    if request.user.is_authenticated:
        from project.orders.models import OrderItem
        qs = OrderItem.objects.filter(user=request.user, ordered=False)
        if qs.exists():
            return qs.count()
        else:
            return 0

    else:
        cart_items = request.session.get('cart', [])
        return len(cart_items)