from django import template

register = template.Library()


@register.filter
def extract_decimal_part(number):
    """
    Custom template filter to extract the decimal part of a number.
    """
    try:
        # Convert the number to a string
        number_str = str(number)

        # Split the string at the decimal point
        parts = number_str.split('.')

        # If there's a decimal part and it's not equal to '0', return it
        if len(parts) == 2 and parts[1] != '0':
            return parts[1]
        else:
            return ''  # Return an empty string if there's no non-zero decimal part
    except TypeError:
        return ''

