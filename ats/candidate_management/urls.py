from django.urls import path
from .views import ListJobs

urlpatterns = [
    path("", ListJobs.as_view(), name='home1'),
    path("home/", ListJobs.as_view(), name='home2')
]