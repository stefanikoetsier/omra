from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import AddSongForm
from .models import Song


def home(request):
    return render(request, 'song_rater/home.html')


def add_song(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = AddSongForm(request.POST)

        if form.is_valid():
            artist = request.POST.get('artist')
            title = request.POST.get('title')

            #  Add song to the database
            Song.objects.create(artist=artist, title=title)

            return HttpResponseRedirect('/song_added')

    else:
        form = AddSongForm()

    return render(request, 'song_rater/add_song.html', {'form': form})


def save_song(request):
    pass


def song_added(request):
    return render(request, 'song_rater/song_added.html')

