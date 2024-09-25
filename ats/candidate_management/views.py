from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from job_management.models import Jobpost
from job_management.forms import JobForm
# Create your views here.


class ListJobs(ListView):
    model = Jobpost
    template_name = "candidate_management/job_page_list.html"
    context_object_name = "jobs"

    def get_queryset(self):
        return Jobpost.objects.filter(is_archived = False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_job_id = self.request.GET.get('selected_job')
        if selected_job_id:
            context['selected_job'] = Jobpost.objects.filter(pk=selected_job_id).first()
        return context


