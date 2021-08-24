from .views import ShopCartViewSet
from rest_framework.routers import DefaultRouter

app_name = "shop_cart"

router = DefaultRouter()
router.register("cart", ShopCartViewSet, basename="shop_cart")

urlpatterns = router.urls
