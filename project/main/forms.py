# forms.py
from django import forms

from project.main.models import Product, ProductImage


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'name'}
                               )
    )


from django.forms.models import inlineformset_factory

ProductImageFormSet = inlineformset_factory(Product, ProductImage, fields=('image', 'name'), extra=1)
