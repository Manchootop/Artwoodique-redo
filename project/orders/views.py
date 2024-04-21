from django import views as views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic as generic_views
from project.main.models import Product
from project.orders.forms import CouponForm
from project.orders.models import Order, Coupon, OrderItem
from project.shared.functions import create_ref_code


class CartView(generic_views.ListView):
    template_name = 'orders/cart.html'
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
        coupon_form = CouponForm()
        tables = context.get('tables', [])

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

        context['coupon_form'] = coupon_form
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
        order_ref_code = create_ref_code()
        order = Order.objects.create(
            user=self.request.user, ordered_date=ordered_date, ref_code=order_ref_code, ordered=False)
        order.save()
        return order

    def _fill_order(self, order):
        order_items = OrderItem.objects.filter(user=self.request.user, ordered=False)
        for order_item in order_items:
            if order_item.item_id not in order.items.all():
                order.items.add(order_item)
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
                return redirect("checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")

class OrderListView(LoginRequiredMixin, generic_views.ListView):
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    model = Order

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context.get('orders', [])
        orders = orders.filter(user=self.request.user)

        context['orders'] = orders
        return context
