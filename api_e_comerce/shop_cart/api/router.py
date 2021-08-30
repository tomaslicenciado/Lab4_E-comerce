from rest_framework.routers import DefaultRouter
from .views import ShopCartModelViewSet, AddProdShopCartModelViewSet

router_cart = DefaultRouter()

router_cart.register(prefix='shopCart', basename='shopCart', viewset=ShopCartModelViewSet)
router_cart.register(prefix='addProd', basename='addProd', viewset=AddProdShopCartModelViewSet)