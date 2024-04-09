from django import template

from project.main.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

# in a templatetags/custom_filters.py


register = template.Library()

@register.filter
def extract_decimal_part(number):
    """
    Custom template filter to extract the decimal part of a number.
    """
    decimal_part = number % 1
    return decimal_part if decimal_part != 0 else ''