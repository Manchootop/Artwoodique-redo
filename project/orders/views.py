import random
import string
from django import views as views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import generic as generic_views
from project.accounts.models import Address
from project.main.models import Product
from project.orders.forms import RefundForm, CouponForm, CheckoutForm
from project.orders.models import Order, Coupon, Refund, OrderItem
from project.shared.functions import is_valid_form

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

# class CheckoutView(views.View):
#     def get(self, *args, **kwargs):
#         # product = Product.objects.get(pk=self.kwargs['slug'])


# class CheckoutView(LoginRequiredMixin, generic_views.TemplateView):
#     template_name = 'checkout.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['products'] =
#         return context

# class CheckoutView(views.View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             form = CheckoutForm()
#             context = {
#                 'form': form,
#                 'couponform': CouponForm(),
#                 'order': order,
#                 'DISPLAY_COUPON_FORM': True
#             }
#
#             shipping_address_qs = Address.objects.filter(
#                 user=self.request.user,
#                 address_type='S',
#                 default=True
#             )
#             if shipping_address_qs.exists():
#                 context.update(
#                     {'default_shipping_address': shipping_address_qs[0]})
#
#             billing_address_qs = Address.objects.filter(
#                 user=self.request.user,
#                 address_type='B',
#                 default=True
#             )
#             if billing_address_qs.exists():
#                 context.update(
#                     {'default_billing_address': billing_address_qs[0]})
#             return render(self.request, "checkout.html", context)
#
#         except ObjectDoesNotExist:
#             messages.info(self.request, "You do not have an active order")
#             return redirect("/")
#
#     def post(self, *args, **kwargs):
#         form = CheckoutForm(self.request.POST or None)
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             if form.is_valid():
#
#                 use_default_shipping = form.cleaned_data.get(
#                     'use_default_shipping')
#                 if use_default_shipping:
#                     print("Using the default shipping address")
#                     address_qs = Address.objects.filter(
#                         user=self.request.user,
#                         address_type='S',
#                         default=True
#                     )
#                     if address_qs.exists():
#                         shipping_address = address_qs[0]
#                         order.shipping_address = shipping_address
#                         order.save()
#                     else:
#                         messages.info(
#                             self.request, "No default shipping address available")
#                         return redirect('/')
#                 else:
#                     print("User is entering a new shipping address")
#                     shipping_address1 = form.cleaned_data.get(
#                         'shipping_address')
#                     shipping_address2 = form.cleaned_data.get(
#                         'shipping_address2')
#                     shipping_country = form.cleaned_data.get(
#                         'shipping_country')
#                     shipping_zip = form.cleaned_data.get('shipping_zip')
#
#                     if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
#                         shipping_address = Address(
#                             user=self.request.user,
#                             street_address=shipping_address1,
#                             apartment_address=shipping_address2,
#                             country=shipping_country,
#                             zip=shipping_zip,
#                             address_type='S'
#                         )
#                         shipping_address.save()
#
#                         order.shipping_address = shipping_address
#                         order.save()
#
#                         set_default_shipping = form.cleaned_data.get(
#                             'set_default_shipping')
#                         if set_default_shipping:
#                             shipping_address.default = True
#                             shipping_address.save()
#
#                     else:
#                         messages.info(
#                             self.request, "Please fill in the required shipping address fields")
#
#                 use_default_billing = form.cleaned_data.get(
#                     'use_default_billing')
#                 same_billing_address = form.cleaned_data.get(
#                     'same_billing_address')
#
#                 if same_billing_address:
#                     billing_address = shipping_address
#                     billing_address.pk = None
#                     billing_address.save()
#                     billing_address.address_type = 'B'
#                     billing_address.save()
#                     order.billing_address = billing_address
#                     order.save()
#
#                 elif use_default_billing:
#                     print("Using the defualt billing address")
#                     address_qs = Address.objects.filter(
#                         user=self.request.user,
#                         address_type='B',
#                         default=True
#                     )
#                     if address_qs.exists():
#                         billing_address = address_qs[0]
#                         order.billing_address = billing_address
#                         order.save()
#                     else:
#                         messages.info(
#                             self.request, "No default billing address available")
#                         return redirect('/')
#                 else:
#                     print("User is entering a new billing address")
#                     billing_address1 = form.cleaned_data.get(
#                         'billing_address')
#                     billing_address2 = form.cleaned_data.get(
#                         'billing_address2')
#                     billing_country = form.cleaned_data.get(
#                         'billing_country')
#                     billing_zip = form.cleaned_data.get('billing_zip')
#
#                     if is_valid_form([billing_address1, billing_country, billing_zip]):
#                         billing_address = Address(
#                             user=self.request.user,
#                             street_address=billing_address1,
#                             apartment_address=billing_address2,
#                             country=billing_country,
#                             zip=billing_zip,
#                             address_type='B'
#                         )
#                         billing_address.save()
#
#                         order.billing_address = billing_address
#                         order.save()
#
#                         set_default_billing = form.cleaned_data.get(
#                             'set_default_billing')
#                         if set_default_billing:
#                             billing_address.default = True
#                             billing_address.save()
#
#                     else:
#                         messages.info(
#                             self.request, "Please fill in the required billing address fields")
#
#                 payment_option = form.cleaned_data.get('payment_option')
#
#                 if payment_option == 'S':
#                     return redirect('payment', payment_option='stripe')
#                 elif payment_option == 'P':
#                     return redirect('payment', payment_option='paypal')
#                 else:
#                     messages.warning(
#                         self.request, "Invalid payment option selected")
#                     return redirect('checkout')
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("order-summary")


class CartView(generic_views.ListView):
    template_name = 'cart.html'
    context_object_name = 'tables'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # If the user is authenticated, get the cart items from the database
        if self.request.user.is_authenticated:
            return OrderItem.objects.filter(user=self.request.user, ordered=False)
        # If the user is not authenticated, get the products from the session
        else:
           return OrderItem.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        tables = context.get('tables', [])
        total_price = 0

        # If the user is authenticated, retrieve corresponding Product instances
        if self.request.user.is_authenticated:
            product_ids = [item.item_id for item in tables]
            products = Product.objects.filter(pk__in=product_ids)
            # handle the order by creating it/filling it with OrderItem instances
            self._handle_order()

            total_price = sum(float(product.current_price()) for product in products)
        else:
            # For unauthenticated users, retrieve Product instances from session['cart']
            cart_item_ids = self.request.session.get('cart', [])
            products = Product.objects.filter(pk__in=cart_item_ids)
            total_price = sum(float(product.current_price()) for product in products)

        context['total'] = total_price
        context['tables'] = products

        return context

    def _handle_order(self):
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]

            self._fill_order(order)

        else:
            # if the user is authenticated, and doesn't have an active order, create one
            order = self._create_order()
            self._fill_order(order)

    def _create_order(self):
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=self.request.user, ordered_date=ordered_date)
        order.save()
        return order
    def _fill_order(self, order):
        order_items = OrderItem.objects.filter(user=self.request.user, ordered=False)
        for order_item in order_items:
            if order_item.item_id not in order.items.all():
                order.items.add(order_item)

class OrderSummaryView(LoginRequiredMixin, views.View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("checkout")

class AddCouponView(views.View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("cart")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("cart")

# class RequestRefundView(views.View):
#     def get(self, *args, **kwargs):
#         form = RefundForm()
#         context = {
#             'form': form
#         }
#         return render(self.request, "request_refund.html", context)
#
# def post(self, *args, **kwargs):
#     form = RefundForm(self.request.POST)
#     if form.is_valid():
#         ref_code = form.cleaned_data.get('ref_code')
#         message = form.cleaned_data.get('message')
#         email = form.cleaned_data.get('email')
#         # edit the order
#         try:
#             order = Order.objects.get(ref_code=ref_code)
#             order.refund_requested = True
#             order.save()
#
#             # store the refund
#             refund = Refund()
#             refund.order = order
#             refund.reason = message
#             refund.email = email
#             refund.save()
#
#             messages.info(self.request, "Your request was received.")
#             return redirect("request-refund")
#
#         except ObjectDoesNotExist:
#             messages.info(self.request, "This order does not exist.")
#             return redirect("request-refund")
