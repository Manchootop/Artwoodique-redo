from django import template

from project.engagements.models import WishList

register = template.Library()


@register.filter
def wishlist_item_count(request):
    if request.user.is_authenticated:
        qs = WishList.objects.filter(user=request.user)
        if qs.exists():
            return qs.count()
        else:
            return 0

    else:
        cart_items = request.session.get('wishlist', [])
        return len(cart_items)