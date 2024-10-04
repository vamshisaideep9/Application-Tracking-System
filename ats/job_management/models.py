from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# Helps in categorizing job postings
class Category(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Specifies the skills, education, and experience  
class Requirement(models.Model):
    skill = models.CharField(max_length=255)
    education = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.skill
    
class JobType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Foreign key to category and Many-to-Many relationships with requirement
class Jobpost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobposts")

    title = models.CharField(max_length=30)
    description = models.TextField()

    is_remote = models.BooleanField(default=False)
    city = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Job Type
    job_type = models.ManyToManyField(JobType, related_name='jobposts')

    # Pay
    min_pay = models.DecimalField(max_digits=10, decimal_places=2)
    max_pay = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField()

    # Automatically set the current date when a job post is created
    posted_at = models.DateField(auto_now_add=True)

    is_archived = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='jobposts', default=1)
    # Each job is associated with a category

    # Many-to-Many Relationship
    requirements = models.ManyToManyField(Requirement, related_name='jobposts')

    def __str__(self):
        return f"{self.title} ({self.job_type.all()}) - {self.city or 'Remote'}"
