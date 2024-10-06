from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from .forms import CandidateSignupForm, EmployerSignupForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'is_candidate', 'is_employer', 'admin', 'is_staff']
    list_filter = ['is_candidate', 'is_employer', 'admin', 'is_staff']
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_candidate', 'is_employer')}
        ),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Roles', {'fields': ('is_candidate', 'is_employer')}),
        ('Permissions', {'fields': ('admin', 'is_staff')}),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password1'):
          obj.set_password(form.cleaned_data['password1'])  
          obj.is_candidate = form.cleaned_data.get('is_candidate', False)
          obj.is_employer = form.cleaned_data.get('is_employer', False)
        obj.save()  

admin.site.register(User, UserAdmin)
