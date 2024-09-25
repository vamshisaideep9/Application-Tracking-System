from django.urls import path
from .views import JobCreateView, SuccessView, JobPostUpdateView, JobListView, JobDeleteView, ArchiveJob, ArchivedJobList, restore_job

urlpatterns = [
    path('', JobListView.as_view(), name='home'),
    path('delete/<int:pk>', JobDeleteView.as_view(), name='delete'),
    path('archive/<int:pk>', ArchiveJob, name='job_archive'),
    path('archived/', ArchivedJobList.as_view(), name='archived'),
    path('restore/<int:pk>', restore_job, name='restore'),
    path('create-job/', JobCreateView.as_view(), name='job_create_step_1'),
    path('update/<int:pk>', JobPostUpdateView.as_view(), name='review_job_post'),
    path('success/', SuccessView.as_view(), name='success')
]
