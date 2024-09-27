from django.urls import path
from .views import ListJobs, upload_file, TemplateView
from accounts.views import CandidateSignupView
from django.contrib.auth.views import LogoutView
app_name = 'candidate_management'

urlpatterns = [
    path("", ListJobs.as_view(), name='home1'),
    path("home/", ListJobs.as_view(), name='home2'),
    path("upload/", upload_file, name='upload'),
    path("apply/", TemplateView.as_view(), name="apply"),
    path("sign-up/", CandidateSignupView.as_view(), name="candidate-sign-up"),
    path('logout/', LogoutView.as_view(next_page='candidate_management:home2'), name='logout'),
]