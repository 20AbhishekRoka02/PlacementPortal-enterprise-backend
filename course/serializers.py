from rest_framework.serializers import ModelSerializer
from .models import Course, Batch

class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ReadCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'semester', 'years']

class UpdateCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'semester', 'years']

class BatchSerializer(ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
        

class ReadBatchSerializer(ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'batch_name']