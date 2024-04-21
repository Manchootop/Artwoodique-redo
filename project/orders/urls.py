from django.urls import path

from project.orders import views
from project.orders.add_to_cart import add_cart
from project.orders.remove_from_cart import remove_cart

urlpatterns = [
    # path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
    path('add-to-cart/<slug>/', add_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_cart, name='remove-from-cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('my_orders/', views.OrderListView.as_view(), name='my_orders'),
]
