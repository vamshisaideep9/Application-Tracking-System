from django.contrib import messages 
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, TemplateView
from job_management.models import Jobpost
from .models import Document, Candidate, Application
from django.core.mail import send_mail
from django.conf import settings
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
    model = Application  
    form_class = CandidateForm
    template_name = "candidate_management/user_apply.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Jobpost, id=job_id)
        context['job'] = job

    
        try:
            candidate = Candidate.objects.get(user=self.request.user)
        except Candidate.DoesNotExist:
            candidate = None 

        form = self.form_class(instance=candidate)
        if candidate:
            form.fields['email_address'].initial = candidate.email_address  # Autofill email_address
        else:
            form.fields['email_address'].initial = self.request.user.email  # Or use the user's email   

        context['form'] = form

        return context

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Jobpost, id=job_id)

        # Check if the user has already applied for this job
        if Application.objects.filter(candidate__user=self.request.user, job=job).exists():
            form.add_error(None, "You have already applied for this job.")
            return self.form_invalid(form)

        # If the candidate doesn't exist, create one
        candidate, created = Candidate.objects.get_or_create(user=self.request.user)

        # Update candidate data
        form_data = form.save(commit=False)
        candidate.full_name = form_data.full_name
        candidate.contact_number = form_data.contact_number
        candidate.email_address = form_data.email_address
        candidate.location = form_data.location
        candidate.technical_skills = form_data.technical_skills
        candidate.non_technical_skills = form_data.non_technical_skills
        candidate.education = form_data.education
        candidate.work_experience = form_data.work_experience
        candidate.save()  # Save the candidate

        # Create the application instance
        application = Application(
            candidate=candidate,
            job=job,
            status='Applied',  # Initial status
        )
        application.save()

        # Send a confirmation email
        send_mail(
            subject='Application Received',
            message=f'Hi {candidate.email_address}, your application for {job.title} has been received.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[candidate.email_address],
            fail_silently=False,
        )

        messages.success(self.request, "Your application has been submitted successfully.")
        return redirect('candidate_management:success', user_id=self.request.user.id)

    def form_invalid(self, form):
        print("Form is invalid")  # Debugging statement
        print(form.errors)  # Print out form errors
        messages.error(self.request, "There was an error in your submission.")
        return super().form_invalid(form)
class SuccessView(TemplateView):
    template_name = "candidate_management/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        context['user'] = user
        return context

class SuccessView(TemplateView):
    template_name = "candidate_management/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        context['user'] = user
        return context




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