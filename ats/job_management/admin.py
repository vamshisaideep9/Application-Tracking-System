from django.contrib import admin
from job_management.models import Jobpost, Category, Requirement, JobType

class JobpostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at', 'city', 'min_pay', 'max_pay')
    list_filter = ('is_remote', 'category')
    search_fields = ('title', 'description')

admin.site.register(Jobpost, JobpostAdmin)
admin.site.register(Requirement)
admin.site.register(Category)
admin.site.register(JobType)
