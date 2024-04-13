# forms.py
from django import forms
from django import forms
from django.contrib import messages
from django.core.mail import send_mail

from project import settings
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from project.main.models import Product, ProductImage


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


