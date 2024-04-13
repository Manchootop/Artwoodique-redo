from django.contrib import admin
from django.contrib.auth import get_user_model

from project.accounts.models import ArtwoodiqueUserProfile
UserModel = get_user_model()

# Register your models here.

@admin.register(ArtwoodiqueUserProfile)
class ArtwoodiqueUserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    pass