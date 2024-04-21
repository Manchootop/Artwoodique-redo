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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import ContactForm
from project import settings
from .filters import ProductFilter
from .models import Product, ProductImage
UserModel = get_user_model()


class HomeView(views.TemplateView):
    template_name = 'main/index.html'


class StoreListView(views.ListView):
    model = Product
    template_name = 'main/store.html'
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
            sort_field = 'calculated_price'

        if order == 'desc':
            queryset = queryset.order_by(f'-{sort_field}')
        else:
            queryset = queryset.order_by(sort_field)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Product.objects.filter(in_stock=True).count()
        return context


class CatalogView(views.ListView):
    model = Product
    template_name = 'main/store.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(in_stock=False)
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
        context['count'] = Product.objects.filter(in_stock=False).count()
        context['is_catalog'] = True
        return context


class ProductDetailsView(views.DetailView):
    model = Product
    template_name = 'main/details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object)
        return context


class ContactsView(views.TemplateView):
    template_name = 'main/contact.html'

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
            recipient_list = [settings.EMAIL_HOST_USER]  # Replace with the recipient's email address

            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            # Send a thank you message to the user
            messages.success(request, 'Thank you for contacting us!')

            return redirect('contacts')  # You should define a URL for the success page
        else:
            messages.warning(request, 'Please fill in the required fields correctly.')
            return render(request, self.template_name, {'form': form})


class FAQView(views.TemplateView):
    template_name = 'main/faq.html'


