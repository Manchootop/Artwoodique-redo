from django.urls import path

from project.main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('details/<int:pk>/', views.ProductDetailsView.as_view(), name='catalog-details'),
    path('store/', views.CollectionView.as_view(), name='store'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('like_button/<int:pk>/', views.like_button_view, name='like_button_view'),
    path('like/', views.toggle_like, name='toggle-like'),

    # URL patterns for adding/removing an item to/from the wishlist
    path('wishlist/', views.toggle_wishlist, name='toggle-wishlist'),
    path('get-liked-status/<int:item_id>/', views.get_liked_status, name='get_liked_status'),
]
