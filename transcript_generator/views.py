from django.shortcuts import render
from django.views import View
from .models import Video
from django.conf import settings
import os
import uuid
import dotenv
import subprocess
import assemblyai as aai
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class VideoTranscibeView(View):
    def get(self, request):
        return render(request, "transcript_generator/index.html")

    def post(self, request):
        file = request.FILES.get("VideoFile")
        if not file:
            return render(request, "transcript_generator/index.html", {"error": "No file uploaded."})

        # Save uploaded video
        job_id = str(uuid.uuid4())
        video_dir = os.path.join(settings.MEDIA_ROOT, "uploads/audios/transcript_generator/")
        os.makedirs(video_dir, exist_ok=True)
        video_path = os.path.join(video_dir, f"{job_id}_input.mp4")
        audio_path = os.path.join(video_dir, f"{job_id}_audio.mp3")
        with open(video_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Extract audio using ffmpeg
        try:
            subprocess.run([
                'ffmpeg', '-y', '-i', video_path, '-vn', '-c:a',
                'libmp3lame', '-f', 'mp3', audio_path
            ], check=True, capture_output=True, text=True)
        except Exception as e:
            return render(request, "transcript_generator/index.html", {"error": f"Audio extraction failed: {e}"})

        # Transcribe audio with AssemblyAI
        dotenv.load_dotenv()
        aai.settings.api_key = os.getenv("ASSEMBLY_API_KEY")
        transcriber = aai.Transcriber()
        try:
            transcript_obj = transcriber.transcribe(audio_path)
            transcript_text = transcript_obj.text
        except Exception as e:
            return render(request, "transcript_generator/index.html", {"error": f"Transcription failed: {e}"})

        # Save to database
        video_entry = Video.objects.create(
            video_file=video_path.replace(os.path.join(settings.MEDIA_ROOT,os.sep), ''),
            audio_file=audio_path.replace(os.path.join(settings.MEDIA_ROOT,os.sep), ''),
            transcript=transcript_text
        )
        return render(request, "transcript_generator/index.html", {"transcript": transcript_text, "video": video_entry})