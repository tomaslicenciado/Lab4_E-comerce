from django.utils.functional import empty
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin
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
    http_method_names = ['patch']

    def partial_update(self, request,pk=None, *args, **kwargs):
        setter_serializer = StockSetterSerializer(isAdd=self.request.data['isAdd'], quantity=self.request.data['quantity'])
        if not (Product.objects.filter(pk=pk).exists()):
            return Response(status=HTTP_400_BAD_REQUEST, data="{error: 'Id de producto ingresado no valido'}")
    
        if setter_serializer.quantity < 0:
            return Response(status=HTTP_400_BAD_REQUEST, data="{error: 'Cantidad ingresada menor a 0'}")
        product = Product.objects.get(pk=pk)
        if setter_serializer.isAdd:
            product.stock_unit = product.stock_unit + setter_serializer.quantity
        else:
            product.stock_unit = setter_serializer.quantity

        product.save()
        ps = ProductSerializer(product)
        return Response(data=ps.data, status=HTTP_200_OK)
        