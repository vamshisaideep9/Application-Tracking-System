from django.db import models
from django.contrib.auth.models import User
from job_management.models import Jobpost
from candidate_management.models import Candidate
# Create your models here.


class InterviewSchedule(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="employer_interviews")
    job = models.ForeignKey(Jobpost, on_delete=models.CASCADE, related_name="job_interviews")
    interview_date = models.DateTimeField(auto_now_add=True)
    calender_event_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.job.title} with {self.candidate.email_address}"