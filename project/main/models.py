from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_countries.fields import CountryField

from django.conf import settings


from project.shared.functions import upload_other_images_product_url
from project.shared.models import TimeBaseModel

UserModel = get_user_model()


def upload_image_product_url(instance, filename):
    return f'product/{instance.title}-product/images/default-image/{filename}'


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

SIZE_CHOICES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
)

TYPE_CHOICES = (
    ('Living Table', 'Living Table'),
    ('Coffe Table', 'Coffe Table'),
    ('Dining Table', 'Dining Table'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Product(models.Model):
    PRICE_MAX_VALUE = 102410241024.00
    PRICE_MIN_VALUE = 0

    discount_price = models.FloatField(
        default=0,
        blank=True,
        null=True
    )
    label = models.CharField(
        default='S',
        choices=LABEL_CHOICES,
        max_length=1
    )
    title = models.CharField(
        max_length=400,
    )

    subheading = models.CharField(
        max_length=400,
        
    )
    description = models.TextField(
        max_length=400,
    )

    material = models.CharField(
        max_length=400,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        editable=False,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.pk}')
        return super().save(*args, **kwargs)

    size = models.CharField(
        max_length=max([len(x) for x, _ in SIZE_CHOICES]),
        choices=SIZE_CHOICES,
        default='undefined',
    )

    type = models.CharField(
        max_length=max([len(x) for x, _ in TYPE_CHOICES]),
        choices=TYPE_CHOICES,
        default='undefined',
    )
    image = models.ImageField(
        upload_to=upload_image_product_url
    )

    views = models.IntegerField(
        default=0
    )

    like = models.IntegerField(
        default=0
    )

    # details = hstore.DictionaryField(
    #     'details of product', default=dict
    # )
    in_stock = models.BooleanField(
        default=True,
    )

    price = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(PRICE_MAX_VALUE),
            MinValueValidator(PRICE_MIN_VALUE)
        ])

    def current_price(self):
        if self.discount_price:
            return f"{self.price - self.discount_price}"
        return self.price

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        print('lolol')
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

    def is_liked_by_user(self, user):
        from project.engagements.models import WishList
        try:
            # Check if the user has liked the item
            self.wishlist_set.get(user=user)
            return True
        except WishList.DoesNotExist:
            return False

    def get_tags(self):
        tags = {
            'material': self.material,
            'size': self.size,
            'type': self.type,

            # TODO: do with details
            # 'details': self.details,
        }
        return tags


class ProductImage(TimeBaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=upload_other_images_product_url
    )

    name = models.CharField(
        max_length=125,
    )

    class Meta:
        db_table = 'images'

    def __str__(self):
        return f'{self.name}:{self.product.title}'


class ProductRating(TimeBaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        default=0
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.product} {self.rating} {self.user}"

    class Meta:
        db_table = 'rating'


# class Sale(models.Model):
#     sale_date = models.DateField()
#     sale_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage discount
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#
#     def has_expired(self):
#         return self.sale_date < timezone.now().date()
#
#     def __str__(self):
#         return f"Sale on {self.sale_date}"



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


