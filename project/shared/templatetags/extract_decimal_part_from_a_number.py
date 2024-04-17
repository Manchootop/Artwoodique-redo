from django import template

register = template.Library()


@register.filter
def extract_decimal_part(number):
    """
    Custom template filter to extract the decimal part of a number.
    """
    try:
        decimal_part = number % 1
    except TypeError:
        decimal_part = 0
    return decimal_part if decimal_part != 0 else ''