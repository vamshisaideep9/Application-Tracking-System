from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from job_management.models import Jobpost
import requests
from .models import EmployerProfile
from accounts.models import User
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests

def linkedin_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if not code or not state:
        return render(request, 'jobboards/error.html', {'message': 'Missing code or state.'})
    access_token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'client_secret': settings.LINKEDIN_CLIENT_SECRET,
    }

    response = requests.post(access_token_url, data=payload)  

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        employer_profile = EmployerProfile.objects.get(user=request.user)
        employer_profile.linkedin_access_token = access_token
        employer_profile.save()
        return render(request, 'job_management/home.html')  
    else:
        return render(request, 'jobboards/error.html', {'message': 'Failed to retrieve access token.'})


from django.urls import reverse
import json
import time
import logging
logging.basicConfig(level=logging.DEBUG)

def post_job_to_linkedin(request, job_id):
    job_post = get_object_or_404(Jobpost, id=job_id)
    employer_profile = get_object_or_404(EmployerProfile, user=request.user)
    access_token = employer_profile.linkedin_access_token

    company_apply_url = request.build_absolute_uri(reverse('candidate_management:upload', args=[job_post.id]))
    job_data_json = {
        "elements": [{
            "integrationContext": f"urn:li:organization:{settings.LINKEDIN_COMPANY_ID}",
            "companyApplyUrl": company_apply_url,
            "description": job_post.description,
            "employmentStatus": job_post.job_type.name if job_post.job_type.name else "Unknown", 
            "externalJobPostingId": str(job_post.id),  
            "listedAt": int(time.time() * 1000), 
            "jobPostingOperationType": "CREATE",
            "title": job_post.title,
            "location" : f"{job_post.city or 'Unknown City'}, {job_post.area or 'Unknown Area'}",
            "workplaceTypes": ["Remote" if job_post.is_remote else "On-site"] ,
            "listingType": "BASIC",
        }]
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Method": "batch_create" 
    }
    response = requests.post(
        "https://api.linkedin.com/v2/simpleJobPostings",
        headers=headers,
        json=job_data_json 
    )

    print(response.status_code)
    print(response.json())
    if response.status_code != 201:
       raise ValueError(f"Failed to post job: {response.text}")
    return redirect('job_management:linkedin-success', job_id=job_id)




def LinkedinSuccess(request, job_id):
    job = Jobpost.objects.get(id=job_id)  
    return render(request, 'jobboards/linkedin_success.html', {'job': job})


from rest_framework import viewsets, permissions
from .serializers import EmployerProfileSerializer

class EmployerLinkedinAccessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print("Access Key:", request.user) 
        return super().list(request, *args, **kwargs)
    