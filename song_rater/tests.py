from django.test import TestCase, Client
from .models import Song


class HomeTestCase(TestCase):
    def test_home_page(self):
        c = Client()
        response = c.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the homepage of Ordina Music Rater')


class AddSongTestCase(TestCase):
    def setUp(self):
        Song.objects.create(artist='Apple', title='pie')

    def test_add_song(self):
        song = Song.objects.get(artist='Apple')
        self.assertEqual(song.title, 'pie')

    def test_add_song_form(self):
        c = Client()
        response = c.get('/add-song')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form action="/add-song" method="post">')
        self.assertContains(response, '<input type="submit" value="Submit">')
