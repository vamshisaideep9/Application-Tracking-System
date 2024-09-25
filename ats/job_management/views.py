from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView
from django.shortcuts import redirect, get_object_or_404
from job_management.models import Jobpost
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .forms import JobForm

# Create your views here.

class JobCreateView(CreateView):
    model = Jobpost
    form_class = JobForm
    template_name = "job_management/job_posting.html"
    success_url = reverse_lazy('review_job_post')

    def form_valid(self, form):
      print(form.cleaned_data)  # Debugging line
      job_post = form.save()
      messages.success(self.request, 'Job post created successfully!')
      return redirect(reverse('review_job_post', kwargs={'pk': job_post.pk}))

class JobPostUpdateView(UpdateView):
    model = Jobpost
    form_class= JobForm
    template_name = 'job_management/review_post.html'
    success_url = reverse_lazy('success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Job Post'
        return context
    
class JobListView(ListView):
    model = Jobpost
    template_name = "job_management/home.html"
    context_object_name = 'jobs'

    def get_queryset(self):
        return Jobpost.objects.filter(is_archived=False)

class ArchivedJobList(ListView):
    model = Jobpost
    template_name = "job_management/archived_job_list.html"
    context_object_name = 'archived_jobs'

    def get_queryset(self):
        return Jobpost.objects.filter(is_archived = True)
    
def restore_job(request, pk):
    job = get_object_or_404(Jobpost, pk=pk)
    job.is_archived = False
    job.save()
    return redirect('home')
        
        

class JobDeleteView(DeleteView):
    model = Jobpost
    template_name = "job_management/job_confirm_delete.html"
    success_url = reverse_lazy('home')



def ArchiveJob(request, pk):
        job = get_object_or_404(Jobpost, pk=pk)
        job.is_archived = True
        job.save()
        return redirect('home')


    
class SuccessView(TemplateView):
    template_name = 'job_management/success.html'


