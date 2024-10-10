from django.contrib import admin
from .models import Jobpost, Category, Requirement, JobType



   
class JobpostAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_types_display', 'city', 'min_pay', 'max_pay', 'posted_at', 'is_archived')

    def job_types_display(self, obj):
        return ", ".join(str(job_type) for job_type in obj.job_type.all())

    job_types_display.short_description = 'Job Types'
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
