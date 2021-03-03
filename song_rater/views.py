from django.shortcuts import render
from django.views.generic.edit import CreateView, FormMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Avg
from django.urls import reverse
from .models import Song
from .forms import RatingForm


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

        song_list = []

        for song in Song.objects.all().prefetch_related('ratings'):
            ratings = song.ratings.all()

            song_list.append({
                'pk': song.pk,
                'artist': song.artist,
                'title': song.title,
                'avg_rating': ratings.aggregate(Avg('rating'))['rating__avg'] or '-',
                'n_ratings': ratings.count(),
            })

        context['song_list'] = song_list

        return context


class SongDetail(FormMixin, DetailView):
    model = Song
    template_name = 'song_rater/song_detail.html'
    form_class = RatingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_list'] = context['song'].ratings.all()
        context['form'] = RatingForm(initial={'post': self.object})

        return context

    def get_success_url(self):
        return reverse('song_rater:song-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        """Bind model instance to self.object for later use in other functions, and add form flow"""
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.song = self.object
        model_instance.save()

        return super().form_valid(form)


def song_added(request):
    return render(request, 'song_rater/song_added.html')
