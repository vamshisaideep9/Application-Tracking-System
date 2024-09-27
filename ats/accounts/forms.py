from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate



User = get_user_model()



class CandidateSignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'password-input',
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'password-input',
    }))

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
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
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password2")

        if password and password_confirm and password != password_confirm:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()  # Save the user to the database
        return user


class CandidateSigninForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255, widget=forms.EmailInput(attrs={
        'placeholder':'Email Address',
        'class':'email-input',
    }))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={
        'placeholder':'password',
        'class' : 'password-input',
    }))
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email does not exist")
        return email




