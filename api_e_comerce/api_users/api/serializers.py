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
        fields = ['username', 'first_name', 'last_name', 'password']

    def update(self, instance, validated_data):
        
        if validated_data['username'] is not None:
            instance.username = validated_data['username']
        if validated_data['first_name'] is not None:
            instance.first_name = validated_data['first_name']
        if validated_data['last_name'] is not None:
            instance.last_name = validated_data['last_name']
        if validated_data['password'] is not None:
            instance.password = make_password(validated_data['password'])
        instance.save()