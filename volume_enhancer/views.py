import os
import uuid
import subprocess
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views import View
from django.conf import settings

JOBS = {}
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class VideoUploadView(View):
    def get(self, request):
        return render(request, "volume_enhancer/upload.html")

    def post(self, request):
        video_file = request.FILES.get('video')
        if not video_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        # Get volume multiplier from form, default to 2.0 if not provided
        try:
            volume = float(request.POST.get('volume', 2.0))
            if volume < 1 or volume > 5:
                volume = 2.0
        except Exception:
            volume = 2.0

        job_id = str(uuid.uuid4())
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        input_path = os.path.join(settings.MEDIA_ROOT, f"{job_id}_input.mp4")
        output_path = os.path.join(settings.MEDIA_ROOT, f"{job_id}_output.mp4")

        with open(input_path, 'wb+') as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        try:
            result = subprocess.run([
                'ffmpeg', '-y', '-i', input_path, '-vcodec', 'copy',
                '-af', f'volume={volume}', output_path
            ], check=True, capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            if os.path.exists(output_path):
                JOBS[job_id] = {'done': True, 'output': output_path}
            else:
                JOBS[job_id] = {'done': False, 'output': None}
        except Exception as e:
            print("ffmpeg error:", e)
            JOBS[job_id] = {'done': False, 'output': None}
        return render(request, "volume_enhancer/status.html", {'job_id': job_id})

def job_status(request, job_id):
    job = JOBS.get(job_id)
    if not job:
        return JsonResponse({'done': False})
    return render(request, "volume_enhancer/status_partial.html", {'job_id': job_id, 'done': job['done']})

def download_video(request, job_id):
    job = JOBS.get(job_id)
    if not job or not job['done']:
        return HttpResponse("Not ready", status=404)
    return FileResponse(open(job['output'], 'rb'), as_attachment=True, filename='enhanced_video.mp4')