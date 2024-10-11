from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EmployerProfile
User = get_user_model()


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['user', 'linkedin_access_token']

