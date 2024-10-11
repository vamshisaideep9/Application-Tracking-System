from django.urls import path
from django.shortcuts import redirect
from .views import CandidateSignupView, CandidateSigninView, EmployerSigninView, EmployerSignupView
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path('candidate-sign-in/', CandidateSigninView.as_view(), name='candidate-sign-in'),
    path('candidate-sign-up/', CandidateSignupView.as_view(), name='candidate-sign-up'),
    path('employer-sign-in/', EmployerSigninView.as_view(), name='employer-sign-in'),
    path('employer-sign-up/', EmployerSignupView.as_view(), name='employer-sign-up'),
     path('login/', lambda request: redirect('accounts:employer-sign-in')),
]