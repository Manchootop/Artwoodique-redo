from django.urls import path

from project.main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('details/<int:pk>/', views.ProductDetailsView.as_view(), name='catalog-details'),
    path('store/', views.StoreListView.as_view(), name='store'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

]
