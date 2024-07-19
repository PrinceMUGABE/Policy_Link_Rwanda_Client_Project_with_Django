from rest_framework import serializers
from .models import UserInstitution

class UserInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInstitution
        fields = ['id', 'user', 'institution', 'created_at']
