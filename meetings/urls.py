from django.urls import path
from .views import create_meeting

urlpatterns = [
    path('create-meeting/', create_meeting, name='create_meeting'),
]
