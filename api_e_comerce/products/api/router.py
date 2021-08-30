from rest_framework.routers import DefaultRouter
from .views import ProductModelViewSet

router_prod = DefaultRouter()

router_prod.register(prefix='products', basename='products', viewset=ProductModelViewSet)
