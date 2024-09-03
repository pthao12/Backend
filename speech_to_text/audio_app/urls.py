from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record_audio, name='record_audio'),
    path('upload/', views.upload_audio, name='upload_audio'),
]
