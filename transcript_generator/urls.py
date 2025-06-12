from django.urls import path
from .views import VideoTranscibeView
from django.conf import settings
from django.conf.urls.static import static
app_name = "transcript_generator"
urlpatterns = [
    path('', VideoTranscibeView.as_view(), name='transcribe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)