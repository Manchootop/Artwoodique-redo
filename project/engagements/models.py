from django.contrib.auth import get_user_model
from django.db import models

from project.main.models import Product

UserModel = get_user_model()


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(
        max_length=100,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# Create your models here.
class ItemLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)


class WishList(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    item = models.ManyToManyField(Product)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s wishlist item: {self.item}"
