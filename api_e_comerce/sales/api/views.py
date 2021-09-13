from products.models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from sales.models import Sale, SaleDetail, PayMethod
from .serializer import SaleSerializer
from shop_cart.api.serializers import ShopCartSerializer, ShopCartDetailSerializer
from shop_cart.models import ShopCart, ShopCartDetail


class SaleModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Sale.objects.filter(user=self.request.user)
        else:
            return Sale.objects.all()

    def create(self, request, *args, **kwargs):
        state = ShopCartDetail.OPEN
        cart = ShopCart.objects.get(user=request.user)
        cart_elem = ShopCartDetail.objects.filter(shopcart=cart, state=state)
        if cart_elem:
            cart_serializer = ShopCartSerializer(cart)
            cart_detail_serializer = ShopCartDetailSerializer(data=cart_serializer.data["details"], many=True)
            cart_detail_serializer.is_valid(raise_exception=True)
            sale = Sale(pay_method=PayMethod.objects.get(id=self.request.data["pm"]), client=self.request.user, delivery_cost=self.request.data["delivery_cost"])
            sale.save()
            for sd in cart_detail_serializer.initial_data:
                prod = Product.objects.get(pk=sd["product"])
                if prod.stock_unit >= sd["quantity"] and sd["state"] == 1:
                    sale_det = SaleDetail(sale=sale, shop_cart_detail=ShopCartDetail.objects.get(pk=sd["id"]))
                    sale_det.save()
            sale = Sale.objects.get(pk=sale.id)
            saleserializer = SaleSerializer(sale)
            return Response(data=saleserializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"El carro de compras está vacío"})
