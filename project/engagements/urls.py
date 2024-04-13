from django.urls import path

from project.engagements import views as views

urlpatterns = [
    path('subscribe/', views.AddSubscriberView.as_view(), name='add_subscriber'),
    path('like_button/<int:pk>/', views.like_button_view, name='like_button_view'),
    path('like/', views.toggle_like, name='toggle-like'),
    # URL patterns for adding/removing an item to/from the wishlist
    path('wishlist/', views.toggle_wishlist, name='toggle-wishlist'),
    path('get-liked-status/<int:item_id>/', views.get_liked_status, name='get_liked_status'),
]