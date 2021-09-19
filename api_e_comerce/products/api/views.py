from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from products.models import Product
from .serializers import ProductSerializer, StockSetterSerializer


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Product.objects.filter(active=True, stock_unit__gt=0)
        else:
            return Product.objects.all()


class SetStockViewSet(ModelViewSet):
    serializer_class = StockSetterSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = StockSetterSerializer(data=self.request.data, many=True, partial=True)
        serializer.is_valid(raise_exception=True)
        for sd in serializer.initial_data:
            prod = Product.get_or_none(pk=sd['id'])
            if not prod:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error : Modificación parcial. El producto de id "+str(sd['id'])+" no existe"})
            elif not prod.active:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"error : Modificación parcial. El producto '"+prod.name+"' no está activo"})
            elif sd['stock_unit'] < 0:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"error : Modificación parcial. Indique una cantidad positivo o 0"})
            else:
                prod.stock_unit = sd['stock_unit']
                prod.save()
        res_serializer = ProductSerializer(Product.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=res_serializer.data)
        