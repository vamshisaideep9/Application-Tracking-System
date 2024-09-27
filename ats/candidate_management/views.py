

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, TemplateView
from job_management.models import Jobpost
from .models import Document, Candidate
from .forms import DocumentForm
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
    
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()  # Save the file to the database
            return redirect('apply')  # Redirect after success
    else:
        form = DocumentForm()

    return render(request, 'candidate_management/upload.html', {'form': form})

class UserApply(TemplateView):
    template_name = 'candidate_management/user_apply.html'


    




