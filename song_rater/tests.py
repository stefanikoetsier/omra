from django.test import TestCase
from .models import Song
import numpy as np


class HomeTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the homepage of Ordina Music Rater')


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


class AddSongTestCase(TestCase):
    def setUp(self):
        test_song = {
            'artist': 'Apple',
            'title': 'Pie'
        }
        add_song(**test_song)

    def test_add_song(self):
        song = Song.objects.get(artist='Apple')
        self.assertEqual(song.title, 'Pie')

    def test_add_song_form(self):
        response = self.client.get('/add-song')
        self.assertEqual(response.status_code, 200)

    def test_add_song_post(self):
        test_song = {
            'artist': 'Strawberry',
            'title': 'Shortcake'
        }
        self.client.post('/add-song', test_song)
        song = Song.objects.get(artist='Strawberry')
        self.assertEqual(song.title, 'Shortcake')

    def test_add_identical_song(self):
        test_song = {
            'artist': 'Blueberry',
            'title': 'Muffin'
        }
        add_song(**test_song)
        response = self.client.post('/add-song', test_song)
        self.assertContains(response, 'Song with this Title and Artist already exists')

    def test_add_song_incomplete_post(self):
        incomplete_song = {
            'artist': 'Orange'
        }
        response = self.client.post('/add-song', incomplete_song)
        self.assertEqual(response.status_code, 200)


class SongListTestCase(TestCase):
    def test_song_list_empty(self):
        response = self.client.get('/song-list')
        self.assertContains(response, 'No songs available yet. Try adding a new song')

    def test_song_list_one_song(self):
        test_values = {
            'artist': 'Apple',
            'title': 'Pie',
            'rating': 3,
        }

        add_song_and_rating(**test_values)
        response = self.client.get('/song-list')

        for value in {*test_values.values()}:  # loop over all test values
            with self.subTest():
                self.assertContains(response, value)

    def test_song_list_multiple_songs(self):
        test_values_1 = {
            'artist': 'Strawberry',
            'title': 'Shortcake',
            'rating': 4
        }
        test_values_2 = {
            'artist': 'Lemon',
            'title': 'Meringue',
            'rating': 3
        }
        add_song_and_rating(**test_values_1)
        add_song_and_rating(**test_values_2)

        response = self.client.get('/song-list')

        for value in {*test_values_1.values(), *test_values_2.values()}:
            with self.subTest():
                self.assertContains(response, value)


class SongDetailTestCase(TestCase):
    def test_rating_list_empty(self):
        test_song = {
            'artist': 'Apple',
            'title': 'Pie',
        }
        test_song = add_song(**test_song)
        response = self.client.get(f'/{test_song.pk}', follow=True)
        self.assertContains(response, 'No ratings available yet. Try adding a new rating')

    def test_rating_list_one_rating(self):
        test_values = {
            'artist': 'Blueberry',
            'title': 'Muffin',
            'rating': 4,
        }
        test_song = add_song_and_rating(**test_values)
        response = self.client.get(f'/{test_song.pk}', follow=True)

        for value in list(test_values.values()):  # loop over all test values
            with self.subTest():
                self.assertContains(response, value)

    def test_rating_list_multiple_ratings(self):
        test_song = {
            'artist': 'Lemon',
            'title': 'Meringue',
        }
        test_song = add_song(**test_song)
        ratings = np.random.randint(low=1, high=6, size=10)

        for rating in ratings:
            add_rating(song=test_song, rating=rating)

        response = self.client.get(f'/{test_song.pk}', follow=True)
        self.assertContains(response, test_song.artist, count=1)
        self.assertContains(response, test_song.title, count=1)

        for rating in ratings:
            with self.subTest():
                self.assertContains(response, rating)
