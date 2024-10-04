from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidate, Application, Document

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        read_only_fields = ['id', 'email']

class DocumentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Document
        fields = ['id', 'user', 'resume']
        read_only_fields = ['id']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        candidate_info = Candidate.objects.create(**validated_data)
        return candidate_info


class ApplicationSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer() 
    job = serializers.StringRelatedField() 

    class Meta:
        model = Application
        fields = [
            'id', 'candidate', 'job', 'status', 'applied_at', 
            'interview_date', 'feedback'
        ]

    def create(self, validated_data):
        candidate_data = validated_data.pop('candidate')
        candidate = Candidate.objects.create(**candidate_data)
        application = Application.objects.create(candidate=candidate, **validated_data)
        return application