from django.test import TestCase
from django.urls import reverse

from .models import Song
import numpy as np


class HomeTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the homepage of Ordina Music Rater')


class AddSongTestCase(TestCase):
    def setUp(self):
        Song.objects.create(artist='Apple', title='Pie')

    def test_add_song(self):
        song = Song.objects.get(artist='Apple')
        self.assertEqual(song.title, 'Pie')

    def test_add_song_form(self):
        response = self.client.get('/add-song')
        self.assertEqual(response.status_code, 200)

    def test_add_song_post(self):
        self.client.post('/add-song', {'artist': 'Strawberry', 'title': 'Shortcake'})
        song = Song.objects.get(artist='Strawberry')
        self.assertEqual(song.title, 'Shortcake')

    def test_add_identical_song(self):
        response = self.client.post('/add-song', {'artist': 'Strawberry', 'title': 'Shortcake'})
        self.assertEqual(response.status_code, 302)

    def test_add_song_incomplete_post(self):
        response = self.client.post('/add-song', {'artist': 'Orange'})
        self.assertEqual(response.status_code, 200)


def add_song(artist: str, title: str) -> Song:
    """Helper function to add a song to the database"""
    return Song.objects.create(artist=artist, title=title)


def add_rating(song: Song, rating: int) -> None:
    """Helper function to add a rating for a song to the database"""
    song.ratings.create(rating=rating)


def add_song_and_rating(artist: str, title: str, rating: int) -> Song:
    """Helper function to add a song and a rating for the same song"""
    song = add_song(artist=artist, title=title)
    add_rating(song=song, rating=rating)

    return song


class SongListTestCase(TestCase):
    def test_song_list_empty(self):
        response = self.client.get('/song-list')
        self.assertContains(response, 'No songs available yet. Try adding a new song')

    def test_song_list_one_song(self):
        add_song_and_rating(artist='Apple', title='Pie', rating=3)

        response = self.client.get('/song-list')
        self.assertContains(response, 'Apple', count=1)
        self.assertContains(response, 'Pie', count=1)
        self.assertContains(response, '3', count=1)  # See if the set average rating is included

    def test_song_list_multiple_songs(self):
        add_song_and_rating(artist='Strawberry', title='Shortcake', rating=4)
        self.test_song_list_one_song()


class SongDetailTestCase(TestCase):
    def test_rating_list_empty(self):
        song = add_song(artist='Apple', title='Pie')
        response = self.client.get(f'/{song.pk}', follow=True)
        self.assertContains(response, 'No ratings available yet. Try adding a new rating')

    def test_rating_list_one_rating(self):
        rating = 4
        song = add_song_and_rating(artist='Blueberry', title='Muffin', rating=rating)
        response = self.client.get(f'/{song.pk}', follow=True)
        self.assertContains(response, song.artist, count=1)
        self.assertContains(response, song.title, count=1)
        self.assertContains(response, rating)

    def test_rating_list_multiple_ratings(self):
        song = add_song(artist='Lemon', title='Meringue')
        ratings = np.random.randint(low=1, high=6, size=10)

        for rating in ratings:
            add_rating(song=song, rating=rating)

        response = self.client.get(f'/{song.pk}', follow=True)
        self.assertContains(response, song.artist, count=1)
        self.assertContains(response, song.title, count=1)

        for rating in ratings:
            self.assertContains(response, rating)


class AddRatingTestCase(TestCase):
    def test_rating_form(self):
        song = add_song(artist='Papaya', title='Icecream')
        ratings = np.ones(shape=10, dtype=int) * 3

        for rating in ratings:
            test_rating = {'rating': rating}
            self.client.post(reverse('song_rater:song-detail', kwargs={'pk': song.pk}), test_rating)

        stored_ratings = list(Song.objects.get(pk=song.pk).ratings.values_list('rating', flat=True))

        self.assertCountEqual(ratings, stored_ratings)

    def test_rating_form_invalid_rating(self):
        song = add_song(artist='Maracuya', title='Sueño')
        test_rating = {'rating': 100}

        self.client.post(reverse('song_rater:song-detail', kwargs={'pk': song.pk}),
                         test_rating, follow=True)
        stored_ratings = list(Song.objects.get(pk=song.pk).ratings.values_list('rating', flat=True))

        self.assertCountEqual([], stored_ratings)
