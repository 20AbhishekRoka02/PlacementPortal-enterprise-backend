from .models import Job, Application
from rest_framework.serializers import ModelSerializer

class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'