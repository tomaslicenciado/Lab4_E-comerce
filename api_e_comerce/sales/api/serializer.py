from rest_framework.serializers import ModelSerializer
from sales.models import Sale, SaleDetail


class SaleDetailSerializer(ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = "__all__"


class SaleSerializer(ModelSerializer):
    detail = SaleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = "__all__"
