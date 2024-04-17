from django import template

from project.engagements.models import WishList

register = template.Library()


@register.filter
def wishlist_item_count(request):
    if request.user.is_authenticated:
        wishlist = WishList.objects.get(user=request.user)
        if wishlist:
                return wishlist.item.count()
        else:
            return 0

    else:
        cart_items = request.session.get('wishlist', [])
        return len(cart_items)