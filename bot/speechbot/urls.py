from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recognize/', views.recognize_speech, name='recognize_speech'),  
    path('recognize_audio/', views.recognize_audio, name='recognize_audio'),
]