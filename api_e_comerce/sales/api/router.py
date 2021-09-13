from rest_framework.routers import DefaultRouter
from .views import SaleModelViewSet, DirectSaleModelViewSet

router_sales = DefaultRouter()

router_sales.register(prefix='sales', basename='sales', viewset=SaleModelViewSet)
router_sales.register(prefix='directSale', basename='directSale', viewset=DirectSaleModelViewSet)
