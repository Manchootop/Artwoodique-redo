from rest_framework import serializers

from project.main.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['material', 'size', 'type', 'title']

class AllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'