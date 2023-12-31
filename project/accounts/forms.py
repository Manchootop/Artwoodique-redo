from django.contrib.auth import forms as auth_forms, get_user_model
# from phonenumber_field.formfields import PhoneNumberField
from django import forms

from project.accounts.models import ArtwoodiqueUserProfile

UserModel = get_user_model()


class UserRegisterForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=ArtwoodiqueUserProfile.FIRST_NAME_MAX_LENGTH)
    last_name = forms.CharField(max_length=ArtwoodiqueUserProfile.LAST_NAME_MAX_LENGTH)
    date_of_birth = forms.DateField()
    gender = forms.ChoiceField(choices=ArtwoodiqueUserProfile.GENDERS)

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = ArtwoodiqueUserProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender'],
            user=user,
        )
        if commit:
            profile.save()
        return user

    class Meta:
        model = UserModel
        fields = ('password1', 'password2', 'first_name', 'last_name', 'gender')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'date_of_birth': forms.DateInput(attrs={'min': '1920-01-01'}),
        }


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['gender'] = ArtwoodiqueUserProfile.DO_NOT_SHOW

    class Meta:
        model = ArtwoodiqueUserProfile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'date_of_birth': forms.DateInput(attrs={'min': '1920-01-01'}),
        }


class UserRegisterForm1(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=ArtwoodiqueUserProfile.FIRST_NAME_MAX_LENGTH,
    )

    last_name = forms.CharField(
        max_length=ArtwoodiqueUserProfile.LAST_NAME_MAX_LENGTH,
    )

    date_of_birth = forms.DateField()

    gender = forms.ChoiceField(
        choices=ArtwoodiqueUserProfile.GENDERS,
    )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = ArtwoodiqueUserProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name',)

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
        }


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        pass

    class Meta:
        model = ArtwoodiqueUserProfile
        fields = ()
