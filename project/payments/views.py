import uuid

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from project.main.models import Product
from project.orders.models import Order


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

def CheckoutView(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = Order.objects.filter(user=request.user, ordered=False)
    products = order.items.all()
    host = request.get_host()


    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'products': products,
        'amount': [item.current_price() for item in products],
        'invoices': uuid.uuid4(),
        'currency': 'USD',
        'notify_url': f'https://{host}{reverse("paypal-ipn")}',
        'return_url': f'https://{host}{reverse("index", kwargs = {'order_id': order.id})}', #TODO: do checkout-success
        'cancel_url': f'https://{host}{reverse("index", kwargs = {'order_id'})}'
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'product': product,
        'paypal_form': paypal_payment,
    }

    return render(request, 'checkout.html', context)