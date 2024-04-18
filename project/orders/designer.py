from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from project.main.models import Product
from project.orders.serializers import ProductSerializer


class SimilarProductsAPIView(APIView):
    permission_classes = [AllowAny]  # Adjust permissions as needed

    @staticmethod
    def get(self, request, *args, **kwargs):
        material = request.query_params.get('material')
        size = request.query_params.get('size')
        type = request.query_params.get('type')

        grouped_products = {}

        if material:
            material_products = Product.objects.filter(material=material)
            serializer = ProductSerializer(material_products, many=True)
            grouped_products['material'] = serializer.data

        if size:
            size_products = Product.objects.filter(size=size)
            serializer = ProductSerializer(size_products, many=True)
            grouped_products['size'] = serializer.data

        if type:
            type_products = Product.objects.filter(type=type)
            serializer = ProductSerializer(type_products, many=True)
            grouped_products['type'] = serializer.data

        return Response(grouped_products)