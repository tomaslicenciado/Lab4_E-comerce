from api_e_comerce.products.api.serializers import ProductSerializer
from api_e_comerce.products.models import Product
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthenticatedOrAdminReadOnly
from sales.models import Sale, SaleDetail, PayMethod
from .serializer import SaleSerializer, SaleDetailSerializer
from shop_cart.api.serializers import ShopCartSerializer, ShopCartDetailSerializer
from shop_cart.models import ShopCart


class SaleModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Sale.objects.filter(user=self.request.user)
        else:
            return Sale.objects.all()

    def create(self, request, *args, **kwargs):
        cart_serializer = ShopCartSerializer(ShopCart.objects.get(id = self.request.data["id"]))
        cart_detail_serializer = ShopCartDetailSerializer(data = cart_serializer.data["details"], many=True)
        cart_detail_serializer.is_valid(raise_exception=True)
        sale = Sale(pay_method=self.request.data["pm"], client=self.request.user, subtotal=cart_serializer.data["subtotal"])
        detailist = []
        for sd in cart_detail_serializer.data:
            prod = ProductSerializer(Product.objects.get(pk = sd["product"]))
            if  prod["stock_unit"] >= sd["quantity"]:
                detailist.append(SaleDetail(product = sd["product"], quantity = sd["quantity"], subtotal = sd["subtotal"], sale = sale.pk, shop_cart_detail = sd["id"]))
                prod["stock_unit"] = prod["stock_unit"] - sd["quantity"]
                if prod["stock_unit"] == 0:
                    prod["active"] = False
                prod.save()
        saleserializer = SaleSerializer(sale)
        Response(data=saleserializer.data, status=status.HTTP_200_OK)


        return Response(data = cart_detail_serializer.data)    
        
        # if self.request.user == serializer.validated_data['user']:
        #     serializer.save()
        #     return Response(status=status.HTTP_200_OK, data=serializer.data)
        # else:
        #     return Response({"error":"El usuario no tiene permiso para crear una venta en esta cuenta"})


