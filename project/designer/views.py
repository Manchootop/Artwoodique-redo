from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from project.designer.serializers import ProductSerializer, AllProductSerializer
from project.main.models import Product, SIZE_CHOICES, TYPE_CHOICES, MATERIAL_CHOICES



class SimilarProductsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'designer/designer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['size_choices'] = SIZE_CHOICES
        context['material_choices'] = MATERIAL_CHOICES
        context['type_choices'] = TYPE_CHOICES
        return context

class SimilarProductsSearchView(APIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            input_product_data = serializer.validated_data
            # Extract input data
            material = input_product_data.get('material')
            size = input_product_data.get('size')
            type = input_product_data.get('type')
            # Get similar products based on each criteria
            similar_material = self.get_similar_material(material)
            similar_size = self.get_similar_size(size)
            similar_type = self.get_similar_type(type)
            # Serialize the similar products
            similar_material_serializer = AllProductSerializer(similar_material, many=True)
            similar_size_serializer = AllProductSerializer(similar_size, many=True)
            similar_type_serializer = AllProductSerializer(similar_type, many=True)
            return Response({
                'similar_material': similar_material_serializer.data,
                'similar_size': similar_size_serializer.data,
                'similar_type': similar_type_serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_similar_material(product_material):
        # Filter products by similar material
        similar_material_products = Product.objects.filter(material=product_material, in_stock=True)
        return similar_material_products

    @staticmethod
    def get_similar_size(product_size):
        # Filter products by similar size
        similar_size_products = Product.objects.filter(size=product_size, in_stock=True)
        return similar_size_products
    @staticmethod
    def get_similar_type(product_type):
        # Filter products by similar type
        similar_type_products = Product.objects.filter(type=product_type, in_stock=True)
        return similar_type_products