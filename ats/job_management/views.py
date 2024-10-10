from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .models import Jobpost
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from candidate_management.models import Application, Candidate

from .forms import JobForm

# Create your views here.

class JobCreateView(CreateView):
    model = Jobpost
    form_class = JobForm
    template_name = "job_management/job_posting.html"
    success_url = reverse_lazy('job_management:review_job_post')

    def form_valid(self, form):
      job_post = form.save(commit=False)
      job_post.user = self.request.user
      job_post.save()
      job_post = form.save()
      messages.success(self.request, 'Job post created successfully!')
      return redirect(reverse('job_management:review_job_post', kwargs={'pk': job_post.pk}))

class JobPostUpdateView(UpdateView):
    model = Jobpost
    form_class= JobForm
    template_name = 'job_management/review_post.html'
    success_url = reverse_lazy('job_management:success')

    def get_queryset(self):
        return Jobpost.objects.filter(user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Job Post'
        return context
    
class JobListView(ListView):
    model = Jobpost
    template_name = "job_management/home.html"
    context_object_name = 'jobs'

    def get_queryset(self):
        return Jobpost.objects.filter(user = self.request.user, is_archived=False)

class ArchivedJobList(ListView):
    model = Jobpost
    template_name = "job_management/archived_job_list.html"
    context_object_name = 'archived_jobs'

    def get_queryset(self):
        return Jobpost.objects.filter(user = self.request.user, is_archived = True)
    
def restore_job(request, pk):
    job = get_object_or_404(Jobpost, pk=pk, user=request.user)
    job.is_archived = False
    job.save()
    return redirect('job_management:home')
        
        

class JobDeleteView(DeleteView):
    model = Jobpost
    template_name = "job_management/job_confirm_delete.html"
    success_url = reverse_lazy('job_management:home')

    def get_queryset(self):
        return Jobpost.objects.filter(user=self.request.user)



def ArchiveJob(request, pk):
        job = get_object_or_404(Jobpost, pk=pk, user = request.user)
        job.is_archived = True
        job.save()
        return redirect('job_management:home')
    
class SuccessView(TemplateView):
    template_name = 'job_management/success.html'


class BeforeHome(TemplateView):
    template_name = 'job_management/before_home.html'

from django.contrib.auth.mixins import LoginRequiredMixin

class JobApplication(LoginRequiredMixin, TemplateView):
    template_name = 'job_management/job_applications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        employer_jobs = Jobpost.objects.filter(user = current_user)
        applications = Application.objects.filter(job__in = employer_jobs)
        context['applications'] = applications
        return context
    
class JobpostDetailView(DetailView):
    model = Jobpost
    template_name = 'job_management/view_job_details.html'
    context_object_name = 'job'

class CandidateDetailView(DeleteView):
    model = Candidate
    template_name = 'job_management/view_candidate_detail.html'
    context_object_name = 'candidate'





from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Category, Requirement, JobType, Jobpost
from .serializers import UserSerializer, CategorySerializer, RequirementSerializer, JobTypeSerializer, JobPostSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print("User:", request.user) 
        return super().list(request, *args, **kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class JobTypeViewSet(viewsets.ModelViewSet):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class JobPostViewSet(viewsets.ModelViewSet):
    queryset = Jobpost.objects.all().select_related('user','category').prefetch_related('job_type','requirements')
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    

    @action(detail=True, methods = ['post'], permission_classes=[permissions.IsAuthenticated])
    def archive(self, request, pk=None):
        jobpost = self.get_object()
        if jobpost.user != request.user:
            return Response({'detail':'Not authorized to archive this job post.'}, status=403)
        jobpost.is_archived=True
        jobpost.save()
        return Response({'status':'Job post archived'})
    

