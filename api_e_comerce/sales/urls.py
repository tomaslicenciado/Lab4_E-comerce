from django.db import router
from django.urls import path

from .views import SalesViewSet
from rest_framework.routers import DefaultRouter

app_name = "sales"

router = DefaultRouter()

router.register("sales", SalesViewSet, basename="sales")

urlpatterns = router.urls