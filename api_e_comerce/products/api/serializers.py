from django.db import models
from rest_framework.serializers import ModelSerializer, Serializer
from products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StockSetterSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'stock_unit']
