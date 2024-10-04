from django.urls import path, include
from .views import JobCreateView, SuccessView, JobPostUpdateView, JobListView, JobDeleteView, ArchiveJob, ArchivedJobList, restore_job, BeforeHome
from django.contrib.auth.views import LogoutView

from rest_framework.routers import DefaultRouter


from .views import (UserViewSet,
                    CategoryViewSet,
                    RequirementViewSet,
                    JobTypeViewSet,
                    JobPostViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'requirements', RequirementViewSet)
router.register(r'jobtypes', JobTypeViewSet)
router.register(r'jobposts', JobPostViewSet)

app_name = 'job_management'

urlpatterns = [
    path('api/', include(router.urls)),
    path('job-post/', JobListView.as_view(), name='home'),
    path('', BeforeHome.as_view(), name="home2"),
    path('delete/<int:pk>', JobDeleteView.as_view(), name='delete'),
    path('archive/<int:pk>', ArchiveJob, name='job_archive'),
    path('archived/', ArchivedJobList.as_view(), name='archived'),
    path('restore/<int:pk>', restore_job, name='restore'),
    path('create-job/', JobCreateView.as_view(), name='job_create_step_1'),
    path('update/<int:pk>', JobPostUpdateView.as_view(), name='review_job_post'),
    path('success/', SuccessView.as_view(), name='success'),
    path('logout/', LogoutView.as_view(next_page='job_management:home2'), name='logout'),
]


