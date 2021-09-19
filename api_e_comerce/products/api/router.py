from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from .views import ProductModelViewSet, SetStockViewSet

router_prod = DefaultRouter()

router_prod.register(prefix='products', basename='products', viewset=ProductModelViewSet)
router_prod.register(prefix='setAddStock', basename='setAddStock', viewset=SetStockViewSet)
