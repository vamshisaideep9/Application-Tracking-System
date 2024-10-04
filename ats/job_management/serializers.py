from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Jobpost, JobType, Category, Requirement

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        read_only_fields = ['id', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'department']
        read_only_fields = ['id']

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['id', 'skill', 'education', 'experience']
        read_only_fields = ['id']

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['id', 'name']
        read_only_fields = ['id']

class JobPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    job_type = serializers.PrimaryKeyRelatedField(queryset=JobType.objects.all(), many=True)
    requirements = serializers.PrimaryKeyRelatedField(queryset=Requirement.objects.all(), many=True)

    class Meta:
        model = Jobpost
        fields = "__all__"
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        job_types = validated_data.pop('job_type')
        requirements = validated_data.pop('requirements')
        jobpost = Jobpost.objects.create(**validated_data)
        jobpost.job_type.set(job_types)
        jobpost.requirements.set(requirements)
        return jobpost
    

    def update(self, instance, validated_data):
        job_types = validated_data.pop('job_type', None)
        requirements = validated_data.pop('requirements', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if job_types is not None:
            instance.job_type.set(job_types)
        
        if requirements is not None:
            instance.requirements.set(requirements)
        
        instance.save()
        return instance

    