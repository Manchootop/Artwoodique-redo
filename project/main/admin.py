from django.contrib import admin
from project.main.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('__all__',)
    readonly_fields = ('views',)
    list_display = ('id', 'title', 'price')
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


