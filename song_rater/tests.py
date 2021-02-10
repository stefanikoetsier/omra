from django.test import TestCase, Client


class HomeTestCase(TestCase):
    def test_home_page(self):
        c = Client()
        response = c.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to the homepage of Ordina Music Rater')
