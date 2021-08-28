from rest_framework import serializers
from .models import Stock, StockDetail


class StockDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StockDetail
        fields = ['product', 'stock', 'quantity', 'subtotal']

class StockSerializer(serializers.ModelSerializer):
    
    details = StockDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ['supplier', 'details']



