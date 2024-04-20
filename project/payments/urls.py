from django.urls import path

from project.payments.views import checkout

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
]