from rest_framework.serializers import ModelSerializer
from .models import Student
from users.serializers import ReadUserSerializer, UpdateUserSerializer
from course.serializers import ReadCourseSerializer, ReadBatchSerializer

class ReadStudentSerializer(ModelSerializer):
    user = ReadUserSerializer(read_only=True)
    course = ReadCourseSerializer(read_only=True)
    batch = ReadBatchSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'


class UpdateStudentSerializer(ModelSerializer):
    user = UpdateUserSerializer()

    class Meta:
        model = Student
        fields = ['user', 'phone_number', 'whatsapp_number', 'course', 'batch']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Update User fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update Student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class CreateStudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'phone_number', 'whatsapp_number', 'course', 'batch']
        extra_kwargs = {
            'user': {'required': True},
            'phone_number': {'required': True},
            'whatsapp_number': {'required': True},
            'course': {'required': True},
            'batch': {'required': True},
        }