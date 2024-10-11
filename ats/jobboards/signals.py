from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import EmployerProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_employer_profile(sender, instance, created, **kwargs):
    if created and instance.is_employer:
        EmployerProfile.objects.create(user=instance)
        print(f'Employer profile created for {instance.email}')
    elif instance.is_employer:
        instance.employerprofile.save()
        print(f'Employer profile updated for {instance.email}')