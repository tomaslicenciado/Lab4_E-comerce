from .views import StockViewSet
from rest_framework.routers import DefaultRouter

app_name = "shop_cart"

router = DefaultRouter()

router.register("stock", StockViewSet, basename="stock")

urlpatterns = router.urls
