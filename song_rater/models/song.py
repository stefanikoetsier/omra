from django.db import models
from django.core.validators import MaxValueValidator


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


class Rating(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
