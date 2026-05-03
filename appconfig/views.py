from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from appconfig.models import SideNavItem
from appconfig.serializers import SideNavItemSerializer
# Create your views here.
@api_view(['GET'])
def get_sidenav_items(request):
    print("request.user: ", request.user)
    sidemenuitems = list()
    if isinstance(request.user, User) and request.user.is_authenticated:
        sidenavitems = SideNavItem.objects.all()
        sidenavitems_data = SideNavItemSerializer(sidenavitems, many=True).data
        return Response({"sidenavitems": sidenavitems_data}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        