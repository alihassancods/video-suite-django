from django.urls import path
from volume_enhancer import views

urlpatterns = [
    path("",views.test,name="test")
]