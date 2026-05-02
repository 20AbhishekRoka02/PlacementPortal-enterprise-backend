from .views import get_sidenav_items
from django.urls import path

urlpatterns = [
    path('sidenavitems/', get_sidenav_items, name='get_sidenav_items'),
]