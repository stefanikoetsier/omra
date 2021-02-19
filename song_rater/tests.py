from django.test import TestCase
from .models import Song


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
        self.assertContains(response, 'Song with this Title and Artist already exists')

    def test_add_song_incomplete_post(self):
        response = self.client.post('/add-song', {'artist': 'Orange'})
        self.assertEqual(response.status_code, 200)


class SongListTestCase(TestCase):
    def setUp(self):
        song = Song.objects.create(artist='Apple', title='Pie')
        song.ratings.create(rating=3)

    def test_song_list(self):
        response = self.client.get('/song-list')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apple', count=1)
        self.assertContains(response, 'Pie', count=1)
        self.assertContains(response, '3', count=1)
