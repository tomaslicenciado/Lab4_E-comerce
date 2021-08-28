from django.shortcuts import render
from stocks.models import Stock, StockDetail
from django.shortcuts import get_object_or_404
from stocks.serializers import StockDetailSerializer, StockSerializer
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.

class StockViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Stock.objects.all()
        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Stock.objects.all()
        stock = get_object_or_404(queryset, pk=pk)
        serializer = StockSerializer(stock)
        return Response(serializer.data)