from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from project.accounts.managers import ArtwoodiqueUserManager


def validate_only_letters(value):
    if not all(ch.isalpha() for ch in value):
        raise ValidationError('Value must contain only letters')


class ArtwoodiqueUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        related_name='user_email'
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        related_name='user_date_joined'
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = ArtwoodiqueUserManager()


class ArtwoodiqueUserProfile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        related_name='user_profile_first_name',
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        related_name='user_profile_last_name',
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW,
        related_name='user_profile_gender'
    )

    # phone_number = PhoneNumberField()

    user = models.OneToOneField(
        ArtwoodiqueUser,
        on_delete=models.CASCADE,
        primary_key=True
    )

    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)

    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
