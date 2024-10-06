from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate



User = get_user_model()


User = get_user_model()


class BaseSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'password-input',
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'password-input',
    }))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'email-input',
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2= cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data

class CandidateSignupForm(BaseSignupForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_candidate = True
        if commit:
            user.save()
        return user

class EmployerSignupForm(BaseSignupForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_employer = True
        if commit:
            user.save()
        return user

class BaseSigninForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255, widget=forms.EmailInput(attrs={
        'placeholder':'Email Address',
        'class':'email-input',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class': 'password-input',
    }))

class CandidateSigninForm(BaseSigninForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_candidate=True).exists():
            raise forms.ValidationError("Email does not exist or is not a candidate.")
        return email

class EmployerSigninForm(BaseSigninForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_employer=True).exists():
            raise forms.ValidationError("Email does not exist or is not an employer.")
        return email