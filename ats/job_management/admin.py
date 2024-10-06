from django.contrib import admin
from .models import Jobpost, Category, Requirement, JobType


class JobpostAdmin(admin.ModelAdmin):
   
    list_display = ('title', 'user', 'city', 'start_date', 'is_archived')
    list_filter = ('is_archived', 'job_type', 'city')
    search_fields = ('title', 'city')
    filter_horizontal = ('job_type', 'requirements')
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name', 'department')


class RequirementAdmin(admin.ModelAdmin):
    list_display = ('skill', 'education', 'experience')
    search_fields = ('skill',)


class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Jobpost, JobpostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Requirement, RequirementAdmin)
admin.site.register(JobType, JobTypeAdmin)
