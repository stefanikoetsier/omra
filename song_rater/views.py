from django.shortcuts import render


def home(request):
    return render(request, 'song_rater/home.html')

