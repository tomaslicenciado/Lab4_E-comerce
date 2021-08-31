from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly
from products.models import Product
from .serializers import ProductSerializer


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Product.objects.filter(active=True, stock_unit__gt=0)
        else:
            return Product.objects.all()
