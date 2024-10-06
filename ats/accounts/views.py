from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views import View
from django.urls import reverse_lazy 
import os
from .forms import CandidateSignupForm, CandidateSigninForm, EmployerSigninForm, EmployerSignupForm
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.contrib import messages
User = get_user_model()



class CandidateSignupView(CreateView):
    model = User
    form_class = CandidateSignupForm
    template_name = "accounts/candidate-signup.html"
    success_url = reverse_lazy("candidate_management:home1")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.is_candidate = True
        user.save()
        login(self.request, user) 
        return super().form_valid(form)

class CandidateSigninView(View):
    def get(self, request):
        form = CandidateSigninForm()
        return render(request, 'accounts/candidate-signin.html', {'form': form})
    
    def post(self, request):
        form = CandidateSigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_candidate:
                login(request, user)
                return redirect('candidate_management:home1')
            else:
                form.add_error(None, "Invalid email or password")
        return render(request, 'accounts/candidate-signin.html', {"form": form})

class EmployerSignupView(CreateView):
    model = User
    form_class = EmployerSignupForm
    template_name = "accounts/employer-signup.html"  
    success_url = reverse_lazy("job_management:home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.is_employer = True
        print(f"Assigning roles: is_candidate={user.is_candidate}, is_employer={user.is_employer}")
        user.save()
        login(self.request, user) 
        return super().form_valid(form)

class EmployerSigninView(View):
    def get(self, request):
        form = EmployerSigninForm()
        return render(request, 'accounts/employer-signin.html', {'form': form})
    
    def post(self, request):
        form = EmployerSigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_employer:
                login(request, user)
                return redirect('job_management:home')
            else:
                form.add_error(None, "Invalid email or password")
        return render(request, 'accounts/employer-signin.html', {"form": form})