from rest_framework import viewsets, status
from .models import Student, Resume
from rest_framework.permissions import IsAuthenticated
from .serializers import ReadStudentSerializer, UpdateStudentSerializer, CreateStudentSerializer, ResumeSerializer
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


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Swagger fix
        if getattr(self, 'swagger_fake_view', False):
            return Resume.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return Resume.objects.none()

        return Resume.objects.filter(student__user=self.request.user)

    def get_object(self):
        return Resume.objects.get(student__user=self.request.user)

    # ❌ Disable list
    def list(self, request, *args, **kwargs):
        return Response(
            {"detail": "List not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # ✅ Create (only once)
    def create(self, request, *args, **kwargs):
        if Resume.objects.filter(student__user=request.user).exists():
            return Response(
                {"detail": "Resume already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(student=request.user.student_profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ✅ Retrieve (own resume)
    def retrieve(self, request, *args, **kwargs):
        try:
            resume = self.get_object()
        except Resume.DoesNotExist:
            return Response(
                {"detail": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(resume)
        return Response(serializer.data)

    # ✅ Update
    def update(self, request, *args, **kwargs):
        resume = self.get_object()
        serializer = self.get_serializer(resume, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # ✅ Partial Update
    def partial_update(self, request, *args, **kwargs):
        resume = self.get_object()
        serializer = self.get_serializer(resume, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # ✅ Delete
    def destroy(self, request, *args, **kwargs):
        resume = self.get_object()
        resume.delete()
        return Response(
            {"detail": "Resume deleted successfully"},
            status=status.HTTP_200_OK
        )
