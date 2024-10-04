from django.contrib import messages 
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, TemplateView
from job_management.models import Jobpost
from django.contrib.auth.decorators import login_required
from .models import Document, Candidate
# Create your views here.




class ListJobs(ListView):
    model = Jobpost
    template_name = "candidate_management/job_page_list.html"
    context_object_name = "jobs"

    def get_queryset(self):
        queryset = Jobpost.objects.filter(is_archived=False)

        title_query = self.request.GET.get('q', '')
        if title_query:
            queryset = queryset.filter(title__icontains=title_query)

        location_query = self.request.GET.get('location', '').strip()
        if location_query:
            if 'remote' in location_query.lower():
                queryset = queryset.filter(is_remote=True)
            else:
                queryset = queryset.filter(city__icontains=location_query)
        return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_job_id = self.request.GET.get('selected_job')
        if selected_job_id:
            context['selected_job'] = Jobpost.objects.filter(pk=selected_job_id).first()
        return context

from .forms import CandidateForm


class UserApply(CreateView):
    model = Candidate
    form_class = CandidateForm
    template_name = "candidate_management/user_apply.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Jobpost, id=job_id)
        context['job'] = job

        # Check if the candidate profile already exists
        candidate = Candidate.objects.filter(user=self.request.user).first()
        if candidate:
            context['form'] = self.form_class(instance=candidate)  # Autofill the form with existing data
        else:
            context['form'] = self.form_class()  # Create a new form if no candidate exists

        return context

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Jobpost, id=job_id)
        candidate = form.save(commit=False)
        candidate.job = job
        candidate.user = self.request.user
        candidate.save()
        return super().form_valid(form)

    def get_success_url(self):
         return reverse('candidate_management:success', kwargs={'user_id': self.request.user.id})

    
class SUccessView(TemplateView):
    template_name = "candidate_management/success.html"




from rest_framework import viewsets, permissions
from rest_framework.decorators import action    
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import DocumentSerializer, CandidateSerializer
from job_management.permissions import IsOwnerOrReadOnly


User = get_user_model()

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()