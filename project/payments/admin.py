from django.contrib import admin

from project.payments.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__email']