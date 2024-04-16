from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
import json

from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from ..shared.functions import previous_page_redirect

from django.shortcuts import get_object_or_404, redirect
from django import views as views
from django.views.decorators.http import require_POST
from django.conf import settings
from project.engagements.forms import NewsletterSignupForm
from project.engagements.models import ItemLike, WishList, Subscriber
from project.main.models import Product


class AddSubscriberView(views.View):
    """
    Add a new subscriber to the database.
    """

    @staticmethod
    def post(request, *args, **kwargs):
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                # Handle sending confirmation email
                subject = 'Subscription Confirmation'
                message = 'Thank you for subscribing to our newsletter.'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=True)

                # Send a thank you message to the user
                messages.success(request, 'Thank you for subscribing!')
            else:
                # The user is already subscribed
                messages.info(request, 'You are already subscribed to our newsletter.')

                return previous_page_redirect(request)

        else:
            messages.warning(request, 'Enter a valid email.')
            # Redirect back to the previous page
        return previous_page_redirect(request)


def like_button_view(request, pk):
    if request.method == 'POST' and request.is_ajax():
        obj = get_object_or_404(Product, pk=pk)  # Replace YourModel with your model class
        liked = request.POST.get('liked') == 'true'

        if liked:
            # Handle like logic, e.g., increase the like count or mark as liked
            obj.likes += 1
            obj.save()
        else:
            # Handle dislike logic, e.g., decrease the like count or mark as not liked
            obj.likes -= 1
            obj.save()

        return JsonResponse({'success': True, 'likes': obj.likes})

    return JsonResponse({'success': False})


@require_POST
def toggle_like(request):
    item_id = request.POST.get('item_id')
    liked = request.POST.get('liked')

    if item_id and liked is not None:
        item_id = int(item_id)
        liked = int(liked)

        user = request.user
        item = Product.objects.get(id=item_id)

        try:
            item_like = ItemLike.objects.get(user=user, item=item)
        except ItemLike.DoesNotExist:
            item_like = None

        if liked == 1:
            # User wants to like the item
            if not item_like:
                item_like = ItemLike(user=user, item=item)
                item_like.save()

            # Add the item to the wishlist
            wishlist_item, created = WishList.objects.get_or_create(user=user, item=item)
        else:
            # User wants to unlike the item
            if item_like:
                item_like.delete()

            # Remove the item from the wishlist
            WishList.objects.filter(user=user, item=item).delete()

        return JsonResponse({'liked': liked == 1})
    return JsonResponse({'error': 'Invalid data'}, status=400)


from django.http import JsonResponse
import json

from django.core.exceptions import ObjectDoesNotExist


@require_POST
def toggle_wishlist(request):
    user = request.user

    try:
        data = json.loads(request.body.decode('utf-8'))
        item_id = data.get('item_id')

        if item_id is None:
            return JsonResponse({'error': 'Missing item_id in the request body'}, status=400)

        try:
            product = Product.objects.get(pk=item_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=400)

        wishlist, created = WishList.objects.get_or_create(user=user)
        if created:
            # If a new wishlist is created, add the product to it
            wishlist.item.add(product)
            liked = True
        else:
            # If the wishlist already exists, check if the product is in it
            if wishlist.item.filter(pk=item_id).exists():
                # If the product is in the wishlist, remove it
                wishlist.item.remove(product)
                liked = False
            else:
                # If the product is not in the wishlist, add it
                wishlist.item.add(product)
                liked = True

        return JsonResponse({'liked': liked})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data in the request body'}, status=400)


def get_liked_status(request, item_id):
    try:
        # Ensure item_id is an integer
        item_id = int(item_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid item ID'}, status=400)

        # Check if the user has liked the product with the given item_id
    if request.user.is_authenticated:
        liked = WishList.objects.filter(user=request.user, item__id=item_id).exists()

    else:
        print('alabala')
        liked = request.session.get('wishlist', [])
        if item_id in liked:
            liked = True
        else:
            liked = False
    # Return the liked status as JSON
    return JsonResponse({'liked': liked})


class WishListView(ListView):
    queryset = WishList.objects.all()
    template_name = 'account/wishlist.html'
    context_object_name = 'wishlist_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_items = context.get('wishlist_items', [])

        # If the user is authenticated => retrieve corresponding Product instances
        if self.request.user.is_authenticated:
            product_ids = [item.id for item in wishlist_items]
            products = WishList.objects.filter(pk__in=product_ids)
        else:
            # For unauthenticated users => retrieve Product instances from session['cart']
            wishlist_items_ids = self.request.session.get('wishlist', [])
            products = Product.objects.filter(pk__in=wishlist_items_ids)

        context['count'] = products.count()
        context['wishlist_items'] = products

        return context


def remove_from_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        wishlist_item = WishList.objects.filter(user=request.user, item=product)
        if wishlist_item.exists():
            wishlist_item.delete()
            messages.success(request, 'Item removed from wishlist')
        else:
            messages.warning(request, 'Item not in wishlist')
    else:
        wishlist = request.session.get('wishlist', [])
        if pk in wishlist:
            wishlist.remove(pk)
            request.session['wishlist'] = wishlist
            messages.success(request, 'Item removed from wishlist.')
        else:
            messages.warning(request, 'Item not in wishlist.')

    return redirect('my_wishlist')


def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user=request.user)

        if wishlist.item.filter(pk=product.pk).exists():
            wishlist.item.remove(product)
            messages.success(request, 'Item removed from wishlist')
        else:
            wishlist.item.add(product)
            messages.success(request, 'Item added to wishlist')
    else:
        wishlist = request.session.get('wishlist', [])
        if pk in wishlist:
            wishlist.remove(pk)
            messages.warning(request, 'Item removed from wishlist')
        else:
            wishlist.append(pk)
            messages.success(request, 'Item added to wishlist')
        request.session['wishlist'] = wishlist

    return redirect('store')
