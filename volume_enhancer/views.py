from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def test(request):
    from moviepy import VideoFileClip
    video = VideoFileClip("C:\\Users\\Ali hassan\\Desktop\\Video Sound Enhancer\\volume_enhancer\\g.mp4")
    louderVideo = video.with_volume_scaled(5)
    louderVideo.write_videofile("output.mp4")
    return HttpResponse("SUCCESS")
