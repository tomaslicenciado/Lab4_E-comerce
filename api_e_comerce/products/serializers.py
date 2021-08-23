from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'unit_price', 'unit_per_package', 'package_price', 'active', 'category', 'supplier')
