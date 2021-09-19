from django.db import models
from rest_framework.serializers import ModelSerializer, Serializer
from products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StockSetterSerializer(Serializer):
    def __init__(self, quantity=None, isAdd=None):
        self.quantity = int(quantity) 
        self.isAdd = isAdd == "True"
