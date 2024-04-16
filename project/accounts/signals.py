import uuid

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from project.accounts.models import ArtwoodiqueUserProfile

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if not created:
        return


    ArtwoodiqueUserProfile.objects.create(user=instance)

def generate_random_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = uuid.uuid4().hex[:30]
pre_save.connect(generate_random_username, sender=ArtwoodiqueUserProfile)