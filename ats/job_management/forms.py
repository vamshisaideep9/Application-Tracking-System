from django.forms import ModelForm
from job_management.models import Jobpost, JobType, Requirement
from django import forms    

class JobForm(ModelForm):
    job_type = forms.ModelMultipleChoiceField(
        queryset=JobType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    requirements = forms.ModelMultipleChoiceField(
        queryset=Requirement.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Jobpost
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Enter job title', 'class' : 'form-control'}),
            'description' : forms.Textarea(attrs={'rows':5,'placeholder':'Enter job description','class':'form-control'}),
            'min_pay': forms.NumberInput(attrs={
                'placeholder': 'Enter minimum salary',
                'class': 'form-control'
            }),
            'max_pay': forms.NumberInput(attrs={
                'placeholder': 'Enter maximum salary',
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={'placeholder':'Enter city name', 'class':'form-control'}),
            'area':  forms.TextInput(attrs={'placeholder':'Enter Area', 'class':'form-control'}),
            'pincode': forms.NumberInput(attrs={'placeholder':'Enter pincode', 'class':'form-control'}),
            'address': forms.Textarea(attrs={'rows':4,'placeholder':'Enter address', 'class':'form-control'}),

        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Company name must be at least 5 characters long.")
        return title

    def clean_min_pay(self):
        min_pay = self.cleaned_data.get('min_pay')
        if min_pay < 0:
            raise forms.ValidationError("Minimum pay cannot be negative.")
        return min_pay

    def clean_max_pay(self):
        max_pay = self.cleaned_data.get('max_pay')
        min_pay = self.cleaned_data.get('min_pay')
        if max_pay < min_pay:
            raise forms.ValidationError("Maximum pay must be greater than or equal to minimum pay.")
        return max_pay
    
    




   
    

    