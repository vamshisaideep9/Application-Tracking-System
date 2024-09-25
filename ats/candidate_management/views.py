from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
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




