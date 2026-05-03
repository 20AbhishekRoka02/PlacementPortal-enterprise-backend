from django.shortcuts import render
from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer, UpdateCompanySerializer
from rest_framework.response import Response

# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        serializer_classes = {
            'list': CompanySerializer,
            'retrieve': CompanySerializer,
            'update': UpdateCompanySerializer,
            'partial_update': UpdateCompanySerializer,
            'create': CompanySerializer
            }
        print("Serializer: ", self.action)
        return serializer_classes.get(self.action, CompanySerializer)

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
        return Response(UpdateCompanySerializer(instance).data)
