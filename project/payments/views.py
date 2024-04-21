import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from project.main.models import Product
from project.orders.forms import CouponForm
from project.orders.models import Order
from project.shared.functions import create_ref_code

@login_required
def checkout(request):
    order = Order.objects.get(user=request.user, ordered=False)
    if not order.ref_code:
        order.ref_code = create_ref_code()
    else:
        order.ref_code = create_ref_code()
    print(order)
    host = request.get_host()

    if not order:
        messages.warning(request, "Internal server error. Please try again later.")
        return redirect('cart')
    # Prepare the URL parameters


    # Construct the return URL
    return_url = reverse("index")

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'item_name': order.ref_code,
        'amount': order.get_total_with_delivery_fee(),
        'invoices': uuid.uuid4(),
        'currency': 'USD',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': f'https://{host}{return_url}',
        'cancel_url': f'https://{host}{return_url}'
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    total = order.get_total()
    coupon_form = CouponForm()
    context = {
        'order': order,
        'order_item_names': order.get_order_item_names,
        'paypal_form': paypal_payment,
        'total': total,
        'delivery_fee': order.calc_delivery_fee(),
        'total_with_delivery_fee': order.get_total_with_delivery_fee(),
        'coupon_form': coupon_form,
    }

    return render(request, 'payments/checkout.html', context)
