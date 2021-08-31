from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import  ModelViewSet
import rest_framework.status as status
from .serializers import UserRegisterSerializer, UserSerializer, UserChangeAttrSerializer
from api_users.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.hashers import make_password

class UserRegisterModelViewSet(ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        serializer.validated_data['password']=make_password(password)
        user = serializer.save()
        user.set_password(serializer.initial_data['password'])
        retSerializer = UserSerializer(user)
        return Response(status=status.HTTP_201_CREATED, data = retSerializer.data)



class UserChangeAttrModelViewSet(ModelViewSet):
    ## TODO
    serializer_class = UserChangeAttrSerializer
    queryset = []
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['patch']

    def partial_update(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        serializer = UserChangeAttrSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        saved_user = serializer.save()
        retSerializer = UserSerializer(saved_user)
        return Response(status = status.HTTP_200_OK, data=retSerializer.data)

