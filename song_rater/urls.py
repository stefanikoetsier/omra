from django.urls import path
from . import views

app_name = 'song_rater'

urlpatterns = [
    path('home', views.home, name='home'),
    path('add-song', views.add_song, name='add-song'),
    path('song-added', views.song_added, name='song-added'),
]
