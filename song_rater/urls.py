from django.urls import path
from . import views

app_name = 'song_rater'

urlpatterns = [
    path('home', views.home, name='home'),
]
