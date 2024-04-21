from django.urls import path

from project.designer.views import SimilarProductsSearchView, SimilarProductsView

urlpatterns = [
    path('similar_products/', SimilarProductsView.as_view(), name='similar-products'),
    path('', SimilarProductsSearchView.as_view(), name='similar-products-search'),
]