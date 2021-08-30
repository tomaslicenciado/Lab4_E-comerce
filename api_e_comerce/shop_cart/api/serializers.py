from rest_framework.serializers import ModelSerializer
from shop_cart.models import ShopCart, ShopCartDetail


class ShopCartDetailSerializer(ModelSerializer):
    class Meta:
        model = ShopCartDetail
        fields = '__all__'


class ShopCartSerializer(ModelSerializer):
    details = ShopCartDetailSerializer(many=True, read_only=True)

    class Meta:
        model = ShopCart
        fields = '__all__'
