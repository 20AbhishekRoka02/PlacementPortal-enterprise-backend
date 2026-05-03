from .views import CourseViewSet, BatchViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'batch', BatchViewSet, basename='batch')
router.register(r'', CourseViewSet, basename='course')

urlpatterns = [
    path("", include(router.urls)),
]
