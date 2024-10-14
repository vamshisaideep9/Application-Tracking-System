from django.urls import path, include
from .views import ListJobs
from accounts.views import CandidateSignupView
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import (DocumentViewSet, CandidateViewSet, UserApply, SuccessView, ApplicationViewSet,
                     MyJobs, UpdateResume, DeleteResume, AddResume, DeleteApply, JobDetailsView)
from parser.views import upload_file
app_name = 'candidate_management'

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='Document')
router.register(r'candidates', CandidateViewSet, basename='Candidate')
router.register(r'applications', ApplicationViewSet, basename='applications')



urlpatterns = [
    path("", ListJobs.as_view(), name='home1'),
    path("api/", include(router.urls)),
    path("home/", ListJobs.as_view(), name='home2'),
    path("my-jobs/", MyJobs, name='my-jobs'),
    path("upload/<int:job_id>/", upload_file, name='upload'),
    path("apply-jobs/<int:job_id>/", UserApply.as_view(), name="apply"),
    path("update/<int:resume_id>", UpdateResume, name="update-resume"),
    path("delete/<int:resume_id>", DeleteResume, name="delete-resume"),
    path("delete-application/<int:application_id>/", DeleteApply, name='delete-application'),
    path('add-resume/<int:application_id>/', AddResume.as_view(), name='add-resume'),
    path('application-details/<int:application_id>/', JobDetailsView.as_view(), name='application-details'),
    path('success/<int:user_id>/', SuccessView.as_view(), name='success'),
    path("sign-up/", CandidateSignupView.as_view(), name="candidate-sign-up"),
    path('logout/', LogoutView.as_view(next_page='candidate_management:home2'), name='logout'),
]