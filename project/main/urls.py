from django.urls import path

from project.main import views
from project.main.views import CheckoutView, OrderSummaryView, RequestRefundView, PaymentView, \
    remove_single_item_from_cart, remove_from_cart, AddCouponView, add_to_cart

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('details/<int:pk>/', views.ProductDetailsView.as_view(), name='catalog-details'),
    path('store/', views.CollectionView.as_view(), name='store'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('like_button/<int:pk>/', views.like_button_view, name='like_button_view'),
    path('like/', views.toggle_like, name='toggle-like'),

    # URL pattern for adding/removing an item to/from the wishlist
    path('wishlist/', views.toggle_wishlist, name='toggle-wishlist'),
    path('get-liked-status/<int:item_id>/', views.get_liked_status, name='get_liked_status'),
]
