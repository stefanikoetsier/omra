from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models import Avg
from .models import Song, Rating


def home(request):
    return render(request, 'song_rater/home.html')


class SongCreate(CreateView):
    model = Song
    fields = ['artist', 'title']
    success_url = '/song-added'


class SongList(ListView):
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        song_table = []

        for song in Song.objects.all():
            ratings = Rating.objects.filter(song=song)
            n_ratings = ratings.count()
            avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']

            song_table.append({
                'artist': song.artist,
                'title': song.title,
                'avg_rating': avg_rating,
                'n_ratings': n_ratings,
            })

        context['song_table'] = song_table

        return context


def song_added(request):
    return render(request, 'song_rater/song_added.html')
