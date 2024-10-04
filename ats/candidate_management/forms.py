from .models import Document, Candidate
from django import forms




class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['resume']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = "__all__"