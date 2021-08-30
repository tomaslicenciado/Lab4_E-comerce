from rest_framework.response import Response
from rest_framework.viewsets import  ModelViewSet
import rest_framework.status as status
from .serializers import UserRegisterSerializer, UserSerializer
from api_users.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class UserRegisterModelViewSet(ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        retSerializer = UserSerializer(user)
        return Response(status=status.HTTP_201_CREATED, data = retSerializer.data)



class UserChangeAttrModelViewSet(ModelViewSet):
    serializer_class = UserSerializer

