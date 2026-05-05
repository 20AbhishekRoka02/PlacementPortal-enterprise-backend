from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Student, Resume, SocialMediaChoices
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

class ResumeSerializer(ModelSerializer):

    class Meta:
        model = Resume
        exclude = ['student', 'created_at', 'updated_at']
        ref_name = 'StudentResumeSerializer'  # Unique name for Swagger
    # 🔥 Validate Social Media
    def validate_social_media(self, value):
        for item in value:
            if 'username' not in item or 'url' not in item or 'name' not in item:
                raise ValidationError("Invalid social media structure")

            if item['name'] not in SocialMediaChoices.values:
                raise ValidationError("Invalid social media name")

        return value

    # 🔥 Validate Education
    def validate_education(self, value):
        required_fields = ['institution', 'qualification', 'start_year', 'end_year', 'location']

        for item in value:
            for field in required_fields:
                if field not in item:
                    raise ValidationError(f"Missing {field} in education")

        return value

    # 🔥 Validate Experience
    def validate_experience(self, value):
        required_fields = ['company', 'start', 'end', 'role', 'location', 'description']

        for item in value:
            for field in required_fields:
                if field not in item:
                    raise ValidationError(f"Missing {field} in experience")

        return value

    # 🔥 Validate Projects
    def validate_projects(self, value):
        required_fields = ['name', 'start', 'end', 'skills', 'link', 'description']

        for item in value:
            for field in required_fields:
                if field not in item:
                    raise ValidationError(f"Missing {field} in projects")

        return value
