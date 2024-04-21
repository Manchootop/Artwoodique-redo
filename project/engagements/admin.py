from django.contrib import admin

from project.engagements.models import WishList, ItemLike, Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'timestamp')
    search_fields = ('email', 'name')
    readonly_fields = ('timestamp',)


@admin.register(ItemLike)
class ItemLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'liked')
    list_filter = ('liked',)
    search_fields = ('user__username', 'item__name')


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_items', 'added_date')
    search_fields = ('user__username',)

    def get_items(self, obj):
        return ", ".join([str(item) for item in obj.item.all()])

    get_items.short_description = 'Items'