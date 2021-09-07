from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthenticatedOrAdminReadOnly
from rest_framework.permissions import IsAuthenticated
from shop_cart.models import ShopCart, ShopCartDetail
from .serializers import ShopCartSerializer, ShopCartDetailSerializer


class ShopCartModelViewSet(ModelViewSet):
    serializer_class = ShopCartSerializer
    queryset = ShopCart.objects.all()
    permission_classes = [IsAuthenticatedOrAdminReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = ShopCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user == serializer.validated_data['user'] or self.request.user.is_staff:
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=request.data)
        else:
            return Response({"error":"El usuario no tiene permiso para crear el carro de otro usuario"})

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            cart = ShopCart.objects.filter(user=request.user).prefetch_related(Prefetch('details',queryset=ShopCartDetail.objects.filter(state=ShopCartDetail.OPEN)))
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
        serializer = ShopCartDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = serializer.validated_data['shopcart']
        if self.request.user != cart.user:
            return Response({"error":"El usuario no tiene permiso para modificar el carrito de otro usuario"})
        elif not serializer.validated_data['product'].active:
            return Response({"error":"No se puede agregar un producto inactivo"})
        elif serializer.validated_data['product'].stock_unit < serializer.validated_data['quantity']:
            return Response({"error":"No hay suficientes unidades del producto para agregar al carro"})
        else:
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.state = ShopCartDetail.CANCELLED
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
