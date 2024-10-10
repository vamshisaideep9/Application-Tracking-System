from .models import Document, Candidate, Application
from django import forms




class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['resume']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        exclude = ['user', 'job']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email_address'].widget.attrs['readonly'] = True   


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('status', 'interview_date')
    


