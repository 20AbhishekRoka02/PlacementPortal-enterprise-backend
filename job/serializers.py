
from course.serializers import ReadBatchSerializer, ReadCourseSerializer

from .models import Job, Application
from users.models import UserRole
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from student.models import Student, Resume
from company.serializers import (
    ListCompanyWithJobSerializer,
    RetrieveCompanyWithJobSerializer,
    )

class ListJobSerializer(ModelSerializer):
    applied = SerializerMethodField(read_only=True)
    company = ListCompanyWithJobSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'salary', 'location', 'deadline', 'applied']

    def get_applied(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        if request.user.role != UserRole.STUDENT:
            return False

        applied_job_ids = self.context.get('applied_job_ids', set())
        return obj.id in applied_job_ids

class RetrieveJobSerializer(ModelSerializer):
    applied = SerializerMethodField(read_only=True)
    company = RetrieveCompanyWithJobSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'salary', 'location', 'deadline', 'applied']

    def get_applied(self, obj):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        if request.user.role != UserRole.STUDENT:
            return False

        applied_job_ids = self.context.get('applied_job_ids', set())
        return obj.id in applied_job_ids

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

class JobSerializer(ModelSerializer):
    company_name = SerializerMethodField()
    applied = SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id',
            'company_name',
            'title',
            'description',
            'location',
            'salary',
            'deadline',
            'posted_at',
            'updated_at',
            'applied',
        ]

    def get_company_name(self, obj):
        return obj.company.name

    def get_applied(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        if request.user.role != 'student':
            return False

        student = getattr(request.user, 'student_profile', None)
        if not student:
            return False

        applied_job_ids = self.context.get('applied_job_ids')
        if applied_job_ids is not None:
            return obj.id in applied_job_ids

        return Application.objects.filter(student=student, job=obj).exists()

class ApplicationCreateSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job']
        read_only_fields = ['id']


class ApplicationListSerializer(ModelSerializer):
    student_name = SerializerMethodField()
    student_email = SerializerMethodField()
    job_title = SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'student_name', 'student_email', 'job_title', 'applied_at']

    def get_student_name(self, obj):
        full_name = obj.student.user.get_full_name()
        return full_name if full_name else obj.student.user.username

    def get_student_email(self, obj):
        return obj.student.user.email

    def get_job_title(self, obj):
        return obj.job.title


class ResumeSerializer(ModelSerializer):
    class Meta:
        model = Resume
        exclude = ['student', 'created_at', 'updated_at']


class StudentDetailSerializer(ModelSerializer):
    name = SerializerMethodField()
    email = SerializerMethodField()
    resume = ResumeSerializer(read_only=True)
    course = ReadCourseSerializer(read_only=True)
    batch = ReadBatchSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'email',
            'phone_number',
            'whatsapp_number',
            'course',
            'batch',
            'resume',
        ]

    def get_name(self, obj):
        full_name = obj.user.get_full_name()
        return full_name if full_name else obj.user.username

    def get_email(self, obj):
        return obj.user.email


class JobDetailSerializer(ModelSerializer):
    company_name = SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id',
            'company_name',
            'title',
            'description',
            'location',
            'salary',
            'deadline',
            'posted_at',
            'updated_at',
        ]

    def get_company_name(self, obj):
        return obj.company.name


class ApplicationDetailSerializer(ModelSerializer):
    student = StudentDetailSerializer(read_only=True)
    job = JobDetailSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'student', 'job', 'applied_at']