from django.db import models
from django.conf import settings

# Create your models here.

class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    linkedin_access_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s Employer profile"
