from django.urls import path, include
from .authorization import linkedin_page, success_view
from .views import linkedin_callback
from rest_framework.routers import DefaultRouter
from .views import EmployerLinkedinAccessViewSet



router= DefaultRouter()

router.register(r'Linkedinaccess', EmployerLinkedinAccessViewSet)

app_name = 'jobboards'

urlpatterns = [
    path('api/', include(router.urls)),
    path('linkedin/connect/', linkedin_page, name='linkedin-connect'),
    path('linkedin/connect/success/', success_view, name='linkedin-success'),
    path('linkedin/callback', linkedin_callback, name='linkedin-callback'),
]
