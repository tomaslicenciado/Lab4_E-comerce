from rest_framework.routers import DefaultRouter
from .views import ShopCartModelViewSet, ProdShopCartModelViewSet

router_cart = DefaultRouter()

router_cart.register(prefix='shopCart', basename='shopCart', viewset=ShopCartModelViewSet)
router_cart.register(prefix='prodCart', basename='prodCart', viewset=ProdShopCartModelViewSet)