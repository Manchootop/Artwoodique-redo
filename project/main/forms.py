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







