from django.urls import path
from . import views

app_name = 'song_rater'

urlpatterns = [
    path('home', views.home, name='home'),
    path('add-song', views.SongCreate.as_view(), name='add-song'),
    path('song-added', views.song_added, name='song-added'),
    path('song-list', views.SongList.as_view(), name='song-list'),
]
