from rest_framework import serializers
from appconfig.models import SideNavItem

class SideNavItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SideNavItem
        fields = '__all__'