from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from project.shared.functions import upload_other_images_product_url
from project.shared.models import TimeBaseModel


def upload_image_product_url(instance, filename):
    return f'product/{instance.name}-product/images/default-image/{filename}'


# Create your models here.


class Product(models.Model):
    PRICE_MAX_VALUE = 102410241024.00
    PRICE_MIN_VALUE = 0
    name = models.CharField(
        max_length=125,
    )

    subheading = models.CharField(
        max_length=125,
    )
    description = models.TextField(
        max_length=400,
    )

    material = models.CharField(
        max_length=100,

    )
    size = models.CharField(
        max_length=100,
    )

    image = models.ImageField(
        upload_to=upload_image_product_url
    )

    views = models.IntegerField(
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

    # def current_price(self):
    #     if self.sale and not self.sale.has_expired():
    #         return self.price - (self.price * (self.sale.sale_percentage / 100))
    #     return self.price

    class Meta:
        db_table = 'product'

    def __str__(self):
        return f'{self.name}: {self.id}'


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
        return f'{self.name}:{self.product.name}'


class ProductRating(TimeBaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        default=0
    )
    user = models.ForeignKey(
        User,
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


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(
        max_length=100,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
