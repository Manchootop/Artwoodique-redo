# forms.py
from django import forms


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'name'}
                               )
    )
