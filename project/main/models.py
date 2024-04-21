from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


from project.shared.functions import upload_other_images_product_url, upload_image_product_url
from project.shared.models import TimeBaseModel

UserModel = get_user_model()




SIZE_CHOICES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
)

MATERIAL_CHOICES = (
    ('Oak', 'Oak'),
    ('Cherry', 'Cherry'),
    ('Pine', 'Pine'),
    ('Walnut', 'Walnut'),
    ('Mulberry', 'Mulberry'),
)

TYPE_CHOICES = (
    ('Living Table', 'Living Table'),
    ('Coffe Table', 'Coffe Table'),
    ('Dining Table', 'Dining Table'),
)


class Product(models.Model):
    PRICE_MAX_VALUE = 102410241024.00
    PRICE_MIN_VALUE = 0

    discount_price = models.FloatField(
        default=0,
        blank=True,
        null=True,
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
        max_length=max([len(x) for x, _ in MATERIAL_CHOICES]),
        choices=MATERIAL_CHOICES,
        default='undefined',
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        editable=False,
    )

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

    def is_liked_by_user(self, user):
        from project.engagements.models import WishList
        try:
            # Check if the user has liked the item
            self.wishlist_set.get(user=user)
            return True
        except WishList.DoesNotExist:
            return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.pk}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product'


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

# class ProductRating(TimeBaseModel):
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE
#     )
#     rating = models.IntegerField(
#         default=0
#     )
#     user = models.ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return f"{self.product} {self.rating} {self.user}"
#
#     class Meta:
#         db_table = 'rating'
