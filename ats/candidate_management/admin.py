from django.contrib import admin
from .models import Candidate, Document, Application

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'email_address', 'created_at')
    search_fields = ('full_name', 'email_address', 'user__username')
    list_filter = ('created_at',)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'resume', 'uploaded_at', 'job_post')
    search_fields = ('user__username',)
    list_filter = ('uploaded_at',)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'resume','applied_at')
    search_fields = ('candidate__full_name', 'job__title', 'status')
    list_filter = ('status', 'applied_at')

    def mark_as_accepted(modeladmin, request, queryset):
        queryset.update(status='Accepted')
    mark_as_accepted.short_description = "Mark selected applications as accepted"
    actions = [mark_as_accepted]



# Register your models here
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Application, ApplicationAdmin)