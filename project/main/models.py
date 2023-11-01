from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField

from django.conf import settings
from project.shared.functions import upload_other_images_product_url
from project.shared.models import TimeBaseModel


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


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


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

    slug = models.SlugField(
        default='default_text'
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

    # def current_price(self):
    #     if self.sale and not self.sale.has_expired():
    #         return self.price - (self.price * (self.sale.sale_percentage / 100))
    #     return self.price

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


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.email

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


class ItemLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have an `Item` model
    liked = models.BooleanField(default=False)


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    item = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have an `Item` model
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.item.title}"
