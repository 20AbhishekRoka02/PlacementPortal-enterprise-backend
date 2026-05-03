from rest_framework import viewsets
from .models import Student
from .serializers import ReadStudentSerializer, UpdateStudentSerializer, CreateStudentSerializer
from rest_framework.response import Response
from users.models import User

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        serializer_classes = {
            'list': ReadStudentSerializer,
            'retrieve': ReadStudentSerializer,
            'update': UpdateStudentSerializer,
            'partial_update': UpdateStudentSerializer,
            'create': CreateStudentSerializer
            }
        print("Serializer: ", self.action)
        return serializer_classes.get(self.action, ReadStudentSerializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        if isinstance(request.user, User) and request.user.is_authenticated:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({'data': serializer.data})
        return Response({'error': 'Unauthorized'}, status=401)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return the updated data using the READ serializer
        return Response(UpdateStudentSerializer(instance).data)
