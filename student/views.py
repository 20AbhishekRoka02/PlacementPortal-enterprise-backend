from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from users.models import User

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        if isinstance(request.user, User) and request.user.is_authenticated:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({'data': serializer.data})
        return Response({'error': 'Unauthorized'}, status=401)
