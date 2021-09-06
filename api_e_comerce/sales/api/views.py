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
        state = ShopDetailState.objects.get(pk=1)
        cart = ShopCart.objects.get(user=request.user)
        cart_elem = ShopCartDetail.objects.filter(shopcart=cart, state=state)
        if cart_elem:
            cart_serializer = ShopCartSerializer(cart)
            cart_detail_serializer = ShopCartDetailSerializer(data=cart_serializer.data["details"], many=True)
            cart_detail_serializer.is_valid(raise_exception=True)
            # if cart_detail_serializer.
            sale = Sale(pay_method=PayMethod.objects.get(id=self.request.data["pm"]), client=self.request.user, delivery_cost=self.request.data["delivery_cost"])
            sale.save()
            for sd in cart_detail_serializer.initial_data:
                prod = Product.objects.get(pk=sd["product"])
                if prod.stock_unit >= sd["quantity"] and sd["state"] == 1:
                    saleDet = SaleDetail(product=prod, quantity=sd["quantity"], subtotal=sd["subtotal"], sale=sale, shop_cart_detail=ShopCartDetail.objects.get(pk=sd["id"]))
                    saleDet.save()
            sale = Sale.objects.get(pk=sale.id)
            saleserializer = SaleSerializer(sale)
            return Response(data=saleserializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"El carro de compras está vacío"})
