from django.urls import path
from .views import CandidateSignupView, CandidateSigninView

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', CandidateSignupView.as_view(), name="candidate-sign-up"),
    path('sign-in/', CandidateSigninView.as_view(), name="candidate-sign-in"),
]