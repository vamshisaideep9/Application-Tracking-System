from django.db import models
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from job_management.models import Jobpost
from django.utils import timezone

User = get_user_model()

def validate_file_size(value):
    limit = 2 * 1024 * 1024  # 2 MB
    if value.size > limit:
        raise ValidationError("File size cannot exceed 2 MB.")

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate")
    job = models.ManyToManyField(Jobpost, related_name="candidates")  
    full_name = models.CharField(max_length=30, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField() 
    location = models.CharField(max_length=100, blank=True)
    technical_skills = models.TextField(blank=True)
    non_technical_skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name or self.user.username  


class Document(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='documents')
    resume = models.FileField(upload_to="resumes/", validators=[validate_file_size])
    uploaded_at = models.DateTimeField(default=timezone.now)
    job_post = models.ForeignKey(
        Jobpost,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.candidate}'s Resume"

    def get_resume_url(self):
        return self.resume.url if self.resume else None


class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Document, null=True, on_delete=models.SET_NULL, related_name="applications")
    job = models.ForeignKey(Jobpost, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(max_length=50, choices=[
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Interviewed', 'Interviewed'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    ])
    applied_at = models.DateTimeField(auto_now_add=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.title if self.job else 'N/A'}"  
