from django.contrib import admin

from project.engagements import models
# Register your models here.
@admin.register(models.Subscriber)
class SubscriberAdminModel(admin.ModelAdmin):
    pass


admin.site.register(models.ItemLike)
admin.site.register(models.WishList)