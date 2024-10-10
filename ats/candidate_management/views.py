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


from django.core.exceptions import ValidationError

from django.urls import reverse_lazy
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
            form.fields['email_address'].initial = candidate.email_address  
        else:
            form.fields['email_address'].initial = self.request.user.email    

        context['form'] = form

        return context

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Jobpost, id=job_id)

        # Check if the user has already applied for this job
        if Application.objects.filter(candidate__user=self.request.user, job=job).exists():
            form.add_error(None, "You have already applied for this job.")
            return self.form_invalid(form)

        # Get or create the candidate
        candidate, created = Candidate.objects.get_or_create(user=self.request.user)

        # Update candidate information
        candidate.full_name = form.cleaned_data['full_name']
        candidate.contact_number = form.cleaned_data['contact_number']
        candidate.email_address = form.cleaned_data['email_address']
        candidate.location = form.cleaned_data['location']
        candidate.technical_skills = form.cleaned_data['technical_skills']
        candidate.non_technical_skills = form.cleaned_data['non_technical_skills']
        candidate.education = form.cleaned_data['education']
        candidate.work_experience = form.cleaned_data['work_experience']
        candidate.save()

        document = Document.objects.filter(candidate=candidate).last()
        application = Application(
            candidate=candidate,
            job=job,
            resume=document,  
            status='Applied', 
        )
        application.save()

        # Send confirmation email
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
        print("Form is invalid")  
        print(form.errors)  
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



from rest_framework import viewsets, permissions
from rest_framework.decorators import action    
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound, ValidationError
from .serializers import DocumentSerializer, CandidateSerializer, ApplicationSerializer


User = get_user_model()

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            candidate = Candidate.objects.get(user=self.request.user)
        except Candidate.DoesNotExist:
            raise NotFound("Candidate profile not found.")

        job_post_id = self.request.data.get('job_post')
        if job_post_id:
            try:
                job_post = Jobpost.objects.get(id=job_post_id)
            except Jobpost.DoesNotExist:
                raise NotFound("Jobpost not found.")
            serializer.save(candidate=candidate, job_post=job_post)
        else:
            serializer.save(candidate=candidate)


class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        if Candidate.objects.filter(user=self.request.user).exists():
            raise ValidationError("Candidate already exists for this user.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        candidate = Candidate.objects.filter(user=self.request.user).first()
        if candidate:
            return Application.objects.filter(candidate=candidate).order_by('-applied_at')
        return Application.objects.none()

    def perform_create(self, serializer):
        candidate = Candidate.objects.filter(user=self.request.user).first()
        if not candidate:
            raise NotFound("Candidate profile not found.")
        resume_id = self.request.data.get('resume')
        job_id = self.request.data.get('job')
        job = get_object_or_404(Jobpost, id=job_id)

        if resume_id:
            resume = get_object_or_404(Document, id=resume_id, candidate=candidate)
        else:
            raise ValidationError("Resume ID is required.")
        serializer.save(candidate=candidate, resume=resume, job=job)    


