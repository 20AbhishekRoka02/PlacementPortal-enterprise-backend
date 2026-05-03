from rest_framework.serializers import ModelSerializer
from .models import Student
from users.serializers import ReadUserSerializer
from course.serializers import ReadCourseSerializer, ReadBatchSerializer

class StudentSerializer(ModelSerializer):
    user = ReadUserSerializer(read_only=True)
    course = ReadCourseSerializer(read_only=True)
    batch = ReadBatchSerializer(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'