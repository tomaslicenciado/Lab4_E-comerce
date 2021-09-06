from products.api.serializers import ProductSerializer
from products.models import Product
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthenticatedOrAdminReadOnly
from sales.models import Sale, SaleDetail, PayMethod
from .serializer import SaleSerializer, SaleDetailSerializer
from shop_cart.api.serializers import ShopCartSerializer, ShopCartDetailSerializer
from shop_cart.models import ShopCart, ShopDetailState, ShopCartDetail


class SaleModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Sale.objects.filter(user=self.request.user)
        else:
            return Sale.objects.all()

    def create(self, request, *args, **kwargs):
        cart_serializer = ShopCartSerializer(ShopCart.objects.get(user=self.request.user))
        cart_detail_serializer = ShopCartDetailSerializer(data=cart_serializer.data["details"], many=True)
        cart_detail_serializer.is_valid(raise_exception=True)
        sale = Sale(pay_method=PayMethod.objects.get(id=self.request.data["pm"]), client=self.request.user, subtotal=cart_serializer.data["subtotal"], delivery_cost=self.request.data["delivery_cost"])
        detailist = []
        for sd in cart_detail_serializer.validated_data:
            prod = ProductSerializer(sd["product"])
            if prod.data["stock_unit"] >= sd["quantity"] and sd["state"] == ShopDetailState.objects.get(pk=1):
                detailist.append(SaleDetail(product=sd["product"], quantity=sd["quantity"], subtotal=sd["subtotal"], sale=sale, shop_cart_detail=ShopCartDetail.objects.get(pk=sd["id"])))
                prod["stock_unit"] = prod["stock_unit"] - sd["quantity"]
                prod.save()
        saleserializer = SaleSerializer(sale)
        saleserializer.save()
        return Response(data=saleserializer.data, status=status.HTTP_200_OK)
