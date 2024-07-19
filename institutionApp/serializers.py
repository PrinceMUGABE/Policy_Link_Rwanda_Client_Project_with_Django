from rest_framework import serializers
from .models import Institution, Department, Policy, Comment
from userAccount.serializers import CustomUserSerializer

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'type', 'created_at']

class DepartmentSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer()

    class Meta:
        model = Department
        fields = ['id', 'name', 'institution']

class PolicySerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Policy
        fields = ['id', 'name', 'description', 'department']
        


class CommentSerializer(serializers.ModelSerializer):
    policy = PolicySerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'policy', 'description', 'comment_description' , 'created_at']
 