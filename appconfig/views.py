from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from users.models import User, UserRole
from appconfig.models import SideNavItem
from appconfig.serializers import SideNavItemSerializer
# Create your views here.
@api_view(['GET'])
def get_sidenav_items(request):
    sidemenuitems = [
        {
            "name": "Job Postings",
            "screen_name": "job_postings",
        },
        {
            "name": "My Applications",
            "screen_name": "my_applications",
        },
    ]
    if isinstance(request.user, User) and request.user.is_authenticated:

        if request.user.role == UserRole.STUDENT:
            sidemenuitems.append({
                "name": "Resume Generator",
                "screen_name": "Resume Generator",
            })

        return Response({"sidenavitems": sidemenuitems}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        