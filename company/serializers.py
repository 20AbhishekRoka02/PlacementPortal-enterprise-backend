from rest_framework.serializers import ModelSerializer
from users.serializers import ReadUserSerializer, UpdateUserSerializer
from .models import Company

class CompanySerializer(ModelSerializer):
    user = ReadUserSerializer(read_only=True)
    class Meta:
        model = Company
        fields = '__all__'

class ListCompanyWithJobSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']

class RetrieveCompanyWithJobSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'website']

class CreateCompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['user', 'name', 'website', 'hr_phone_number', 'hr_email']
        extra_kwargs = {
            'user': {'required': True},
            'name': {'required': True},
            'website': {'required': True},
            'location': {'required': True},
            'hr_phone_number': {'required': True},
            'hr_email': {'required': True},
        }

class UpdateCompanySerializer(ModelSerializer):
    user = UpdateUserSerializer()

    class Meta:
        model = Company
        fields = ['user', 'name', 'website', 'hr_phone_number', 'hr_email']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Update User fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update Company fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
