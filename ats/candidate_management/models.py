from django.db import models
from job_management.models import Jobpost


# Create your models here.

class Candidate(models.Model):  # Renamed to CamelCase
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Jobpost, on_delete=models.CASCADE, related_name='applications')
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
        return f"{self.candidate} - {self.job}"
