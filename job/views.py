from django.shortcuts import render
from .models import Job, Application
from .serializers import JobSerializer, CreateJobSerializer, UpdateJobSerializer, ApplicationSerializer, CreateApplicationSerializer
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        serializer_classes = {
            'list': JobSerializer,
            'retrieve': JobSerializer,
            'update': UpdateJobSerializer,
            'partial_update': UpdateJobSerializer,
            'create': CreateJobSerializer
            }
        print("Serializer: ", self.action)
        return serializer_classes.get(self.action, JobSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return the updated data using the READ serializer
        return Response(UpdateJobSerializer(instance).data)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()

    def get_serializer_class(self):
        serializer_classes = {
            'list': ApplicationSerializer,
            'retrieve': ApplicationSerializer,
            'create': CreateApplicationSerializer
            }
        print("Serializer: ", self.action)
        return serializer_classes.get(self.action, ApplicationSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})