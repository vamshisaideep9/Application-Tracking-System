from django.contrib import admin
from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CandidateSignupForm

# Register your models here.

User = get_user_model()



class UserAdmin(BaseUserAdmin):
    form = CandidateSignupForm
    
    list_display = ['email', 'is_candidate', 'is_employer', 'admin', 'is_staff']
    list_filter = ['is_candidate', 'is_employer', 'admin', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Roles', {'fields': ('is_candidate', 'is_employer')}),
        ('Permissions', {'fields': ('admin', 'is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_candidate', 'is_employer')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
