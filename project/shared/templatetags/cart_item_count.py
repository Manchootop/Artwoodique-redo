from django import template


register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        from project.orders.models import OrderItem
        qs = OrderItem.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
        else:
            return 0
    else:
        return 0