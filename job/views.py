from django.shortcuts import render
from django.utils import timezone
from .models import Job, Application
from .serializers import (
    ListJobSerializer,
    RetrieveJobSerializer,
    CreateJobSerializer,
    UpdateJobSerializer,
    ApplicationCreateSerializer,
    ApplicationListSerializer,
    ApplicationDetailSerializer)
from student.models import Student
from rest_framework import viewsets
from rest_framework.response import Response
from users.models import User, UserRole
from company.models import Company
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def job_list(request):
    if request.user.is_authenticated:
        jobs = Job.objects.filter(
        ).order_by('-posted_at')

        return render(
            request,
            'jobs/list.html',
            {
                'jobs': jobs
            }
        )

@login_required
def job_detail(request, pk):
    if request.user.is_authenticated:
        job = get_object_or_404(
            Job,
            pk=pk
        )

        return render(
            request,
            'jobs/detail.html',
            {
                'job': job
            }
        )

# API ViewSet
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        serializer_classes = {
            'list': ListJobSerializer,
            'retrieve': RetrieveJobSerializer,
            'update': UpdateJobSerializer,
            'partial_update': UpdateJobSerializer,
            'create': CreateJobSerializer
            }
        return serializer_classes.get(self.action)

    def get_queryset(self):
        # Swagger fix
        if getattr(self, 'swagger_fake_view', False):
            return Job.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return Job.objects.none()

        if user.role == UserRole.COMPANY:
            company = Company.objects.filter(user=user).first()
            if company:
                return Job.objects.filter(company=company)
            return Job.objects.none()

        return Job.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.request.user.is_authenticated and self.request.user.role == UserRole.STUDENT:
            student = getattr(self.request.user, 'student_profile', None)
            if student:
                applied_job_ids = Application.objects.filter(student=student).values_list('job_id', flat=True)
                context['applied_job_ids'] = set(applied_job_ids)

        return context

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.role == UserRole.COMPANY:
            company = Company.objects.filter(user=user).first()
            if not company:
                return Response({'detail': 'Company profile not found'}, status=status.HTTP_404_NOT_FOUND)

            data = request.data.copy()
            request.data['company'] = company.pk

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        serializer = self.get_serializer(self.queryset, many=True)
        return Response({'data': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        job = self.get_object()
        user = request.user

        # COMPANY: can only see their own job
        if user.role == UserRole.COMPANY:
            try:
                company = Company.objects.get(user=user)
            except Company.DoesNotExist:
                return Response({'detail': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

            if job.company_id != company.id:
                return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        # STUDENT: can see all jobs, but not expired ones
        elif user.role == UserRole.STUDENT:
            if job.deadline and job.deadline < timezone.now():
                return Response({'detail': 'Job expired'}, status=status.HTTP_403_FORBIDDEN)

        # (Optional) Other roles → restrict or allow
        else:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(job)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(RetrieveJobSerializer(instance, context=self.get_serializer_context()).data)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()

        # ✅ Only owner company can delete
        if user.role != UserRole.COMPANY or instance.company.user != user:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)

        return Response({'detail': 'Job deleted successfully'}, status=status.HTTP_200_OK)

class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        if self.action == 'list':
            return ApplicationListSerializer
        if self.action == 'retrieve':
            return ApplicationDetailSerializer
        return ApplicationDetailSerializer

    def get_queryset(self):
        # Swagger fix
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()

        user = self.request.user

        if not user.is_authenticated:
            return Application.objects.none()

        # Student sees only own applications
        if user.role == 'student':
            if not hasattr(user, 'student_profile'):
                return Application.objects.none()
            return Application.objects.filter(
                student=user.student_profile
            ).select_related(
                'student', 'student__user', 'job', 'job__company'
            ).prefetch_related('student__resume')

        # Company sees applications only for their own jobs
        if user.role == 'company':
            return Application.objects.filter(
                job__company__user=user   # adjust if your Company model uses a different field
            ).select_related(
                'student', 'student__user', 'job', 'job__company'
            ).prefetch_related('student__resume')

        return Application.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            raise PermissionDenied("Only students can apply for jobs.")

        student = get_object_or_404(Student, user=self.request.user)
        job = serializer.validated_data['job']

        if Application.objects.filter(student=student, job=job).exists():
            raise PermissionDenied("You have already applied for this job.")

        serializer.save(student=student)

    def list(self, request, *args, **kwargs):
        if request.user.role != 'company':
            raise PermissionDenied("Only company users can view the application list.")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        raise PermissionDenied("Update is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise PermissionDenied("Update is not allowed.")

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("Delete is not allowed.")