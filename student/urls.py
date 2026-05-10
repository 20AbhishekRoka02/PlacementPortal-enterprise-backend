from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ResumeViewSet, dashboard, resume, get_resume
router = DefaultRouter()
router.register(r'resume', ResumeViewSet, basename='resume')
router.register(r'profiles', StudentViewSet, basename='student')

urlpatterns = [
    path("", include(router.urls)),
    path('dashboard/', dashboard, name='student_dashboard'),
    path('resume-generator/', resume, name='resume_generator'),
    path('get-resume', get_resume, name='get_resume'),
]
