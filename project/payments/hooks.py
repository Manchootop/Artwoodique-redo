from django.conf import settings
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from project.orders.models import Order, OrderItem


def handle_successful_payment(ipn_obj):
    # Perform necessary actions for a successful payment
    try:
        # Mark the order as paid
        order = Order.objects.get(user=ipn_obj.user, ordered=False)
        order.ordered = True
        order.save()

        # Mark all items associated with the order as ordered
        order_items = OrderItem.objects.filter(order=order)
        order_items.update(ordered=True)

        for order_item in order_items:
            product = order_item.item  # Access the associated product
            # Update properties of the product as needed
            product.in_stock = False
            product.save()  # Save the changes


        messages.success(ipn_obj, "Thank you for your purchase! Table is being delivered.")
    except Order.DoesNotExist:
        messages.error(ipn_obj, "Order not found or already processed.")
    except Exception as e:
        messages.error(ipn_obj, f"Error processing payment: {str(e)}")

@receiver(post_save, sender=valid_ipn_received)
def handle_payment(sender, **kwargs):
    print('alabala')
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            messages.error(ipn_obj, "Internal server error. Please try again later.")
            return redirect('checkout')

        handle_successful_payment(ipn_obj)
        return redirect('index')


valid_ipn_received.connect(handle_payment)


# @receiver(post_save, sender=invalid_ipn_received)
# def handle_invalid_payment(sender, **kwargs):
#     messages.error(sender, "Internal server error. Please try again later.")
#     return redirect('checkout')