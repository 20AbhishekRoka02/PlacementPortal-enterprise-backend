
from .models import Job, Application
from rest_framework.serializers import ModelSerializer
from company.serializers import (
    ListCompanyWithJobSerializer,
    RetrieveCompanyWithJobSerializer,
    )

class ListJobSerializer(ModelSerializer):
    company = ListCompanyWithJobSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'salary', 'location', 'deadline']

class RetrieveJobSerializer(ModelSerializer):
    company = RetrieveCompanyWithJobSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'salary', 'location', 'deadline']

class CreateJobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'location', 'salary', 'deadline']
        extra_kwargs = {
            'company': {'required': True},
            'title': {'required': True},
            'description': {'required': True},
            'location': {'required': True},
            'salary': {'required': False},
            'deadline': {'required': False},
            # 'skill': {'required': False},
        }

class UpdateJobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'deadline']

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class CreateApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['student', 'job']
        extra_kwargs = {
            'student': {'required': True},
            'job': {'required': True},
        }