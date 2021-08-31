from api_users.models import User
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password

class UserRegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name',]

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserChangeAttrSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserChangePasswordSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['password']