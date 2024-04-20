import uuid

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from project.main.models import Product
from project.orders.forms import CouponForm
from project.orders.models import Order
from project.shared.functions import create_ref_code


# class PaymentView(View):
#     def get(self, *args, **kwargs):
#         logger.debug("CheckoutView GET method reached")
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         if order.billing_address:
#             context = {
#                 'order': order,
#                 'DISPLAY_COUPON_FORM': False,
#                 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
#             }
#             userprofile = self.request.user.userprofile
#             if userprofile.one_click_purchasing:
#                 # fetch the users card list
#                 cards = stripe.Customer.list_sources(
#                     userprofile.stripe_customer_id,
#                     limit=3,
#                     object='card'
#                 )
#                 card_list = cards['data']
#                 if len(card_list) > 0:
#                     # update the context with the default card
#                     context.update({
#                         'card': card_list[0]
#                     })
#             return render(self.request, "payment.html", context)
#         else:
#             messages.warning(
#                 self.request, "You have not added a billing address")
#             return redirect("checkout")
#
#     def post(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         form = PaymentForm(self.request.POST)
#         userprofile = UserProfile.objects.get(user=self.request.user)
#         if form.is_valid():
#             token = form.cleaned_data.get('stripeToken')
#             save = form.cleaned_data.get('save')
#             use_default = form.cleaned_data.get('use_default')
#
#             if save:
#                 if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
#                     customer = stripe.Customer.retrieve(
#                         userprofile.stripe_customer_id)
#                     customer.sources.create(source=token)
#
#                 else:
#                     customer = stripe.Customer.create(
#                         email=self.request.user.email,
#                     )
#                     customer.sources.create(source=token)
#                     userprofile.stripe_customer_id = customer['id']
#                     userprofile.one_click_purchasing = True
#                     userprofile.save()
#
#             amount = int(order.get_total() * 100)
#
#             try:
#
#                 if use_default or save:
#                     # charge the customer because we cannot charge the token more than once
#                     charge = stripe.Charge.create(
#                         amount=amount,  # cents
#                         currency="usd",
#                         customer=userprofile.stripe_customer_id
#                     )
#                 else:
#                     # charge once off on the token
#                     charge = stripe.Charge.create(
#                         amount=amount,  # cents
#                         currency="usd",
#                         source=token
#                     )
#
#                 # create the payment
#                 payment = Payment()
#                 payment.stripe_charge_id = charge['id']
#                 payment.user = self.request.user
#                 payment.amount = order.get_total()
#                 payment.save()
#
#                 # assign the payment to the order
#
#                 order_items = order.items.all()
#                 order_items.update(ordered=True)
#                 for item in order_items:
#                     item.save()
#
#                 order.ordered = True
#                 order.payment = payment
#                 order.ref_code = create_ref_code()
#                 order.save()
#
#                 messages.success(self.request, "Your order was successful!")
#                 return redirect("/")
#
#             except stripe.error.CardError as e:
#                 body = e.json_body
#                 err = body.get('error', {})
#                 messages.warning(self.request, f"{err.get('message')}")
#                 return redirect("/")
#
#             except stripe.error.RateLimitError as e:
#                 # Too many requests made to the API too quickly
#                 messages.warning(self.request, "Rate limit error")
#                 return redirect("/")
#
#             except stripe.error.InvalidRequestError as e:
#                 # Invalid parameters were supplied to Stripe's API
#                 print(e)
#                 messages.warning(self.request, "Invalid parameters")
#                 return redirect("/")
#
#             except stripe.error.AuthenticationError as e:
#                 # Authentication with Stripe's API failed
#                 # (maybe you changed API keys recently)
#                 messages.warning(self.request, "Not authenticated")
#                 return redirect("/")
#
#             except stripe.error.APIConnectionError as e:
#                 # Network communication with Stripe failed
#                 messages.warning(self.request, "Network error")
#                 return redirect("/")
#
#             except stripe.error.StripeError as e:
#                 # Display a very generic error to the user, and maybe send
#                 # yourself an email
#                 messages.warning(
#                     self.request, "Something went wrong. You were not charged. Please try again.")
#                 return redirect("/")
#
#             except Exception as e:
#                 # send an email to ourselves
#                 messages.warning(
#                     self.request, "A serious error occurred. We have been notifed.")
#                 return redirect("/")
#
#         messages.warning(self.request, "Invalid data received")
#         return redirect("/payment/stripe/")

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

    return render(request, 'checkout.html', context)
