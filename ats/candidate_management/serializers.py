from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidate, Application, Document
from job_management.models import Jobpost

User = get_user_model()

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'resume', 'uploaded_at', 'job_post')
        read_only_fields = ('id', 'uploaded_at')

    def validate_job_post(self, value):
        if value and not Jobpost.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Jobpost does not exist.")
        return value


class ApplicationSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)
    resume = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all(), required=True)
    job = serializers.PrimaryKeyRelatedField(queryset=Jobpost.objects.all(), required=True)

    class Meta:
        model = Application
        fields = (
            'id',
            'candidate',
            'resume',
            'job',
            'status',
            'applied_at',
            'interview_date',
            'feedback',
        )
        read_only_fields = ('id', 'candidate', 'applied_at')

    def validate_resume(self, value):
        # Ensure the resume belongs to the candidate
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                candidate = Candidate.objects.get(user=request.user)
                if value.candidate != candidate:
                    raise serializers.ValidationError("Resume does not belong to the authenticated candidate.")
            except Candidate.DoesNotExist:
                raise serializers.ValidationError("Candidate profile not found.")
        return value