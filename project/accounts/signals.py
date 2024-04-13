import uuid

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from project.accounts.models import ArtwoodiqueUserProfile

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if not created:
        return


    ArtwoodiqueUserProfile.objects.create(user=instance)


@receiver(post_save, sender=ArtwoodiqueUserProfile)
def generate_username(sender, instance, created, **kwargs):
    if created and not instance.username:
        instance.username = str(uuid.uuid4())[:ArtwoodiqueUserProfile.USERNAME_MAX_LENGTH]
        instance.save()