from django.contrib import admin
from project.main.models import Product, ProductImage, ProductRating


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
