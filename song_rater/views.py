from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
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


class SongDisplay(DetailView):
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_list'] = context['song'].ratings.all()
        context['form'] = RatingForm(initial={'post': self.object})

        return context


class SongInterest(SingleObjectMixin, FormView):
    template_name = 'song_rater/song_detail.html'
    form_class = RatingForm
    model = Song

    def get_success_url(self):
        return reverse('song_rater:song-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.song = self.object
        model_instance.save()

        return super().form_valid(form)


class SongDetail(View):

    def get(self, request, *args, **kwargs):
        view = SongDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SongInterest.as_view()
        return view(request, *args, **kwargs)


def song_added(request):
    return render(request, 'song_rater/song_added.html')
