from django.urls import path
from .views import VideoUploadView, job_status, download_video
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', VideoUploadView.as_view(), name='upload'),
    path('status/<job_id>/', job_status, name='job_status'),
    path('download/<job_id>/', download_video, name='download_video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)