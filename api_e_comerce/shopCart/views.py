from rest_framework import viewsets
from .models import ShopCart
from rest_framework.permissions import IsAuthenticated
from .serializers import ShopCartSerializer
from rest_framework.response import Response

class ShopCartViewSet(viewsets.ModelViewSet):
    queryset = ShopCart.objects.all()
    serializer_class = ShopCartSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == self.request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({"error":"Usuario invalido"})



