from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    amount = models.FloatField()
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.user.email
