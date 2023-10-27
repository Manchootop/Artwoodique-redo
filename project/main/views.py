from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Avg
from django.views import generic as views

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
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(in_stock=True)
        product_filter = ProductFilter(self.request.GET, queryset=queryset)

        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'asc')

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
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        context['count'] = ProductFilter
        return context


class CatalogView(views.ListView):
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        product_filter = ProductFilter(self.request.GET, queryset=queryset)
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order', 'asc')  # Default to ascending order

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
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        context['count'] = ProductFilter
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


class FAQView(views.TemplateView):
    template_name = 'faq.html'
