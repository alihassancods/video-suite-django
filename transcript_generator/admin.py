from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "video_file", "audio_file", "created_at")
    search_fields = ("transcript",)
    readonly_fields = ("transcript",)

# Register your models here.
