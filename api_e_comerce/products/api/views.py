from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from products.models import Product
from .serializers import ProductSerializer


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            serializer = ProductSerializer(Product.objects.filter(active=True), many=True)
            return Response(data=serializer.data)
        else:
            serializer = ProductSerializer(Product.objects.all(), many=True)
            return Response(data=serializer.data)

