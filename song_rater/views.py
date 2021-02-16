from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Song


def home(request):
    return render(request, 'song_rater/home.html')


class SongCreate(CreateView):
    model = Song
    fields = ['artist', 'title']
    success_url = '/song-added'


class SongList(ListView):
    model = Song


def song_added(request):
    return render(request, 'song_rater/song_added.html')
