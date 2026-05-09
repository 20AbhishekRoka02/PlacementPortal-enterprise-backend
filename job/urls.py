from .views import JobViewSet, ApplicationViewSet, job_detail, job_list
from rest_framework.routers import DefaultRouter
from django.urls import path, include
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = [
    path("", include(router.urls)),
     path(
        'job-list',
        job_list,
        name='job_list'
    ),

    path(
        'job-list/<int:pk>/',
        job_detail,
        name='job_detail'
    ),
]