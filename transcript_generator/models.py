from django.db import models
import uuid
# Create your models here.
class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120,default="None")
    video_file = models.FileField(upload_to='uploads/audios/transcript_generator/', blank=True, null=True)
    audio_file = models.FileField(upload_to='uploads/audios/transcript_generator/', blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video - {self.title}"