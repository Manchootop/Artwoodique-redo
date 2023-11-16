# forms.py
from django import forms
from django import forms
from django.contrib import messages
from django.core.mail import send_mail

from project import settings
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from project.main.models import Product, ProductImage, Subscriber


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'name'}
                               )
    )


class ContactForm(forms.Form):
    heading = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'heading'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'})
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),  # You can adjust 'rows' and 'cols' as needed
    )


from django.forms.models import inlineformset_factory

ProductImageFormSet = inlineformset_factory(Product, ProductImage, fields=('image', 'name'), extra=1)

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
