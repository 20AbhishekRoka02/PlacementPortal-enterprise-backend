from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ResumeViewSet, dashboard
router = DefaultRouter()
router.register(r'resume', ResumeViewSet, basename='resume')
router.register(r'profiles', StudentViewSet, basename='student')

urlpatterns = [
    path("", include(router.urls)),
    path('dashboard/', dashboard, name='student_dashboard'),
]
