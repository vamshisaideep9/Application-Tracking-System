from django.shortcuts import render, redirect, get_object_or_404
from candidate_management.models import Candidate, Document
from candidate_management.forms import DocumentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from job_management.models import Jobpost
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
import json

os.environ["GOOGLE_API_KEY"] = "AIzaSyDoMLCl-6zQI76X_wv2wpDcI1pk8bEpmW4"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

def parse_resume(file):
    """Extract text from the resume PDF file."""
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def resumes_details(resume):
    prompt = f"""
    You are a resume parsing assistant. Given the following resume text, extract all the important details and return them in a well-structured JSON format.

    The resume text:
    {resume}

    Extract and include the following:
    - Full Name
    - Contact Number
    - Email Address
    - Location
    - Skills (Technical and Non-Technical, separately if possible)
    - Education
    - Work Experience (including company name, role, and responsibilities)

    Return the response in JSON format.
    """

    try:
        response = model.generate_content(prompt).text
        return response
    except Exception as e:
        print("Error during resume parsing:", str(e))  
        return json.dumps({"error": "Failed to parse resume."}) 
    
@login_required
def upload_file(request, job_id):
    job = get_object_or_404(Jobpost, id=job_id)
    existing_document = Document.objects.filter(user=request.user, job_post=job).first()
    candidate = Candidate.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['resume']

            if not file or file.name == '':
                messages.error(request, 'No selected file.')
                return redirect('candidate_management:apply', job_id=job.id)

            if file.name.endswith('.pdf'):
                resume_text = parse_resume(file)  
                resume_data = resumes_details(resume_text)

                response_clean = resume_data.replace("```json", "").replace("```", "").strip()
             
                try:
                        data = json.loads(response_clean)
                except json.JSONDecodeError as e:
                        messages.error(request, 'Failed to parse resume data. Please check the content of the resume.')
                        print("JSONDecodeError:", str(e))
                        return redirect('candidate_management:apply', job_id=job.id)
                if candidate:
                    candidate.full_name = data.get('Full Name', candidate.full_name)
                    candidate.email_address = request.user.email
                    candidate.contact_number = data.get('Contact Number', candidate.contact_number)
                    candidate.location = data.get('Location', candidate.location)
                    candidate.technical_skills = ', '.join(data.get('Skills', {}).get('Technical Skills', []))  
                    candidate.non_technical_skills = ', '.join(data.get('Skills', {}).get('Non-Technical Skills', []))  
                    candidate.education = "\n".join([f"{edu.get('Degree', 'N/A')} from {edu.get('Institute', 'N/A')} (Graduated: {edu.get('Start Date', 'N/A')} - {edu.get('End Date', 'N/A')})" for edu in data.get("Education", [])])
                    candidate.work_experience = "\n".join([f"{job.get('Role', 'N/A')} at {job.get('Company Name', 'N/A')} ({job.get('Start Date', 'N/A')} - {job.get('End Date', 'N/A')})\nResponsibilities: {', '.join(job.get('Responsibilities', []))}" for job in data.get("Work Experience", [])])
                    candidate.save()
                    messages.success(request, 'Your candidate profile has been updated successfully.')
                    return redirect('candidate_management:apply', job_id=job.id)
                else:
                    candidate = Candidate.objects.create(
                    user=request.user,
                    full_name=data.get('Full Name', ''),
                    email_address = request.user.email,
                    contact_number=data.get('Contact Number', ''),
                    location=data.get('Location', ''),
                    technical_skills=', '.join(data.get('Skills', {}).get('Technical Skills', [])),  
                    non_technical_skills=', '.join(data.get('Skills', {}).get('Non-Technical Skills', [])),  

       
                    education="\n".join([f"{edu.get('Degree', 'N/A')} from {edu.get('Institute', 'N/A')} (Graduated: {edu.get('Start Date', 'N/A')} - {edu.get('End Date', 'N/A')})" for edu in data.get("Education", [])]),
                    work_experience="\n".join([f"{job.get('Role', 'N/A')} at {job.get('Company Name', 'N/A')} ({job.get('Start Date', 'N/A')} - {job.get('End Date', 'N/A')})\nResponsibilities: {', '.join(job.get('Responsibilities', []))}" for job in data.get("Work Experience", [])])
                    
                )    
                messages.success(request, 'Your candidate profile has been created successfully.')
                return redirect('candidate_management:apply', job_id=job.id)
                
            else:
                messages.error(request, 'Invalid file type. Please upload a PDF file.')
                return redirect('candidate_management:apply', job_id=job.id)

        else:
            messages.error(request, 'There was an error with the upload form. Please try again.')

    else:
        form = DocumentForm(instance=existing_document) if existing_document else DocumentForm()

    return render(request, 'candidate_management/upload.html', {
        'form': form,
        'job': job,
        'existing_document': existing_document,
        'candidate': candidate,
       
    })



 