from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from .models import EmployerProfile  
import urllib.parse

import logging

logger = logging.getLogger(__name__)


def linkedin_page(request):
    if request.user.is_authenticated:
        try:
            employer_profile = EmployerProfile.objects.get(user=request.user)
            if employer_profile.linkedin_access_token:
                messages.info(request, "You are already connected to LinkedIn.")
                return redirect('jobboards:linkedin-success')  

        except EmployerProfile.DoesNotExist:
            logger.warning(f"EmployerProfile not found for user: {request.user}")
   

    # Retrieve client_id from settings
    client_id = settings.LINKEDIN_CLIENT_ID 
    print(client_id)
    
    redirect_uri = settings.LINKEDIN_REDIRECT_URI  
    print(redirect_uri)
    
    scope = "profile email w_member_social openid" 
    state = request.user.pk if request.user.is_authenticated else "random_state_string"  

    # Construct the authorization URL
    authorization_url = (
        "https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}&"
        f"state={urllib.parse.quote(str(state))}&scope={urllib.parse.quote(scope)}"
    )

    print(authorization_url)
    return redirect(authorization_url)

def success_view(request):
    return render(request, 'jobboards/success.html') 