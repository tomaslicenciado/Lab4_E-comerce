from django.urls import path

from .views import ProductViewSet
from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User
app_name = "products"

router = DefaultRouter()
router.register("prod", ProductViewSet, basename="products")

urlpatterns = router.urls