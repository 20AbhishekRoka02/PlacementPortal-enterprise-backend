from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ResumeViewSet
router = DefaultRouter()
router.register(r'resume', ResumeViewSet, basename='resume')
router.register(r'', StudentViewSet, basename='student')

urlpatterns = [
    path("", include(router.urls)),
]