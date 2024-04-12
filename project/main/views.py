from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg, ExpressionWrapper, F, FloatField, Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic as views
import random
import string
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, View
from .forms import ContactForm
from .models import ItemLike, WishList
from project import settings
from .filters import ProductFilter
from .forms import NewsletterSignupForm
from .models import Product, ProductImage, ProductRating, Subscriber


class HomeView(views.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsletterSignupForm()
        return context

    def post(self, request, *args, **kwargs):
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

            return self.render_to_response(self.get_context_data(form=form))
        else:
            messages.warning(request, 'Enter a valid email.')
            return self.render_to_response(self.get_context_data(form=form))


class CollectionView(views.ListView):
    model = Product
    template_name = 'store.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(in_stock=True)
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'asc')

        queryset = queryset.annotate(
            calculated_price=ExpressionWrapper(
                Coalesce(F('price') - F('discount_price'), F('price')),
                output_field=FloatField()
            )
        )

        if sort_by == 'price':
            sort_field = 'calculated_price'
        elif sort_by == 'views':
            sort_field = 'views'
        else:
            sort_field = 'calculated_price'  # Replace 'default_sort_field' with the actual default sort field

        if order == 'desc':
            queryset = queryset.order_by(f'-{sort_field}')
        else:
            queryset = queryset.order_by(sort_field)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['paginator'].count
        is_catalog = any(not product.in_stock for product in context['products'])
        context['is_catalog'] = is_catalog

        return context

    # @login_required
    # def dispatch(self, request, *args, **kwargs):
    #     # Check if the user is authenticated
    #
    #     if request.user.is_authenticated:
    #         context = self.get_context_data()
    #         context['liked_products'] = WishList.objects.filter(user=request.user)
    #         return super().dispatch(request, *args, **kwargs)
    #     return super().dispatch(request, *args, **kwargs)


class CatalogView(views.ListView):
    model = Product
    template_name = 'store.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.all()
        product_filter = ProductFilter(self.request.GET, queryset=queryset)
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'asc')  # Default to ascending order

        queryset = queryset.annotate(
            calculated_price=ExpressionWrapper(
                Coalesce(F('price') - F('discount_price'), F('price')),
                output_field=FloatField()
            )
        )
        if sort_by == 'price':
            if order == 'desc':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')
        elif sort_by == 'views':
            if order == 'desc':
                queryset = queryset.order_by('-views')
            else:
                queryset = queryset.order_by('views')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['paginator'].count
        is_catalog = any(not product.in_stock for product in context['products'])
        context['is_catalog'] = is_catalog
        return context


class ProductDetailsView(views.DetailView):
    model = Product
    template_name = 'details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object)
        context['average_rating'] = ProductRating.objects.filter(product=self.object).aggregate(Avg('rating'))[
            'rating__avg']

        # try:
        #     sale = Sale.objects.get(product=self.object)
        #     context['sale_percentage'] = sale.sale_percentage
        #     context['sale_expiry_date'] = sale.sale_date
        # except Sale.DoesNotExist:
        #     context['sale_percentage'] = None
        #     context['sale_expiry_date'] = None

        return context


class ContactsView(views.TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            heading = form.cleaned_data['heading']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # You can handle sending the email here similar to the newsletter signup view
            subject = 'Contact Form Submission'
            message = f'Heading: {heading}\nEmail: {email}\nMessage: {message}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_EMAIL]  # Replace with the recipient's email address

            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            # Send a thank you message to the user
            messages.success(request, 'Thank you for contacting us!')

            return redirect('contacts')  # You should define a URL for the success page
        else:
            messages.warning(request, 'Please fill in the required fields correctly.')
            return render(request, self.template_name, {'form': form})


class FAQView(views.TemplateView):
    template_name = 'faq.html'


UserModel = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


#
# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "products.html", context)





import logging

logger = logging.getLogger(__name__)







def previous_page_redirect(request, cart_url):
    if request.META.get('HTTP_REFERER'):
        request.session['previous_page'] = request.META.get('HTTP_REFERER')
    return redirect(cart_url)


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

        # Try to find matching WishList objects for the user and item_id
        wishlist_items = WishList.objects.filter(user=user, item_id=item_id)

        if wishlist_items.exists():
            # If there are matching objects, remove them
            wishlist_items.delete()
            liked = False
        else:
            try:
                product = Product.objects.get(pk=item_id)
                # If no matching objects, create a new one
                WishList.objects.create(user=user, item=product)
                liked = True
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=400)

        return JsonResponse({'liked': liked})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data in the request body'}, status=400)


def get_liked_status(request, item_id):
    if request.user.is_authenticated:
        # Check if the user has liked the product with the given item_id
        liked = WishList.objects.filter(user=request.user, item_id=item_id).exists()
    else:
        liked = False

    # Return the liked status as JSON
    return JsonResponse({'liked': liked})
