from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User, Group, Permission
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from project.accounts.managers import ArtwoodiqueUserManager
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


def validate_only_letters(value):
    if not value.is_alpha():
        raise ValidationError('Value must contain only letters')


# class ArtwoodiqueUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(
#         unique=True,
#     )
#
#     date_joined = models.DateTimeField(
#         auto_now_add=True,
#     )
#
#     is_staff = models.BooleanField(
#         default=False,
#     )
#
#     USERNAME_FIELD = 'email'
#
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=_('groups'),
#         blank=True,
#         related_name='artwoodiqueuser_set',  # Change this to a unique name
#         related_query_name='user',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name=_('user permissions'),
#         blank=True,
#         related_name='artwoodiqueuser_set',  # Change this to a unique name
#         related_query_name='user',
#         help_text=_('Specific permissions for this user.'),
#     )
#
#     objects = ArtwoodiqueUserManager()

class ArtwoodiqueUser(AbstractBaseUser, PermissionsMixin):
    # password from `AbstractBaseUser`
    # last_login from `AbstractBaseUser`

    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     related_name='artwoodiqueuser_groups',  # Unique related_name
    #     related_query_name='user',
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_('user permissions'),
    #     blank=True,
    #     related_name='artwoodiqueuser_permissions',  # Unique related_name
    #     related_query_name='user',
    #     help_text=_('Specific permissions for this user.'),
    # )

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = 'email'

    objects = ArtwoodiqueUserManager()

    def __str__(self):
        return str(self.email)


class ArtwoodiqueUserProfile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    USERNAME_MIN_LENGTH = 2
    USERNAME_MAX_LENGTH = 30

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(USERNAME_MIN_LENGTH),
        ),
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        ),
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        ),
        blank=False,
        null=False,
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

    )

    # phone_number = PhoneNumberField()

    user = models.OneToOneField(
        ArtwoodiqueUser,
        on_delete=models.CASCADE,
        primary_key=True
    )

    # def __str__(self):
    #     return f'{self.first_name} {self.last_name} with {self.user.email} and id: {self.user.id}'


class Address(models.Model):
    user = models.ForeignKey(ArtwoodiqueUser,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = 'Addresses'
