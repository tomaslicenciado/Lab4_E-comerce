from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthenticatedOrAdminReadOnly
from rest_framework.permissions import IsAuthenticated
from shop_cart.models import ShopCart, ShopCartDetail
from .serializers import ShopCartSerializer, ShopCartDetailSerializer
from products.models import Product


class ShopCartModelViewSet(ModelViewSet):
    serializer_class = ShopCartSerializer
    queryset = ShopCart.objects.all()
    permission_classes = [IsAuthenticatedOrAdminReadOnly]
    http_method_names = ['list']

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            cart = ShopCart.objects.filter(user=request.user).\
                prefetch_related(Prefetch('details', queryset=ShopCartDetail.objects.filter(state=ShopCartDetail.OPEN)))
            if cart:
                serializer = ShopCartSerializer(cart, many=True)
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT, data={"error":"El usuario no tiene carro de compras creado"})
        else:
            serializer = ShopCartSerializer(ShopCart.objects.all(), many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)


class ProdShopCartModelViewSet(ModelViewSet):
    serializer_class = ShopCartDetailSerializer
    queryset = ShopCartDetail.objects.all()
    permission_classes = [IsAuthenticatedOrAdminReadOnly]

    def create(self, request, *args, **kwargs):
        cart_detail = ShopCartDetail.objects.create(product=Product.objects.get(pk=self.request.data["product"]),
                                                    quantity=self.request.data["quantity"],
                                                    shopcart=ShopCart.objects.get(user=self.request.user))
        if not cart_detail.product.active:
            return Response({"error":"No se puede agregar un producto inactivo"})
        elif cart_detail.product.stock_unit < cart_detail.quantity:
            return Response({"error":"No hay suficientes unidades del producto para agregar al carro"})
        else:
            cart_detail.save()
            serializer = ShopCartDetailSerializer(cart_detail)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.state = ShopCartDetail.CANCELED
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
