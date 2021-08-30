from api_users.models import User
from rest_framework.serializers import ModelSerializer

class UserRegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name',]

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserChangeAttrSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
