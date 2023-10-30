from django.contrib import admin
from project.main.models import Product, ProductImage, ProductRating, Subscriber
from .models import OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile


class ProductImageInline(admin.TabularInline):  # Use TabularInline for a table-based layout
    model = ProductImage
    extra = 1  # The number of empty forms displayed


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('__all__',)
    readonly_fields = ('views',)
    list_display = ('id', 'title', 'price')
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    pass


# @admin.register(Sale)
# class SaleAdmin(admin.ModelAdmin):
#     list_display = ('sale_date', 'sale_percentage',)
#     list_filter = ('sale_date',)
#     search_fields = ('sale_date',)
#     ordering = ('-sale_date',)
#     date_hierarchy = 'sale_date'
#     list_editable = ('sale_percentage',)
#
#     def mark_as_expired(modeladmin, request, queryset):
#         for sale in queryset:
#             sale.has_expired = True
#             sale.save()
#
#     mark_as_expired.short_description = "Mark selected sales as expired"
#
#     actions = [mark_as_expired]
#
#
#     fieldsets = (
#         ('Sale Information', {
#             'fields': ('sale_date', 'sale_percentage'),
#         }),
#         ('Status', {
#             'fields': ('has_expired',),
#         }),
#     )
@admin.register(Subscriber)
class SubscriberAdminModel(admin.ModelAdmin):
    pass


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
