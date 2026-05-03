from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ReadUserSerializer(ModelSerializer):
    class Meta:
        model =  User
        fields = ['id', 'first_name', 'last_name', 'email']

class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']
