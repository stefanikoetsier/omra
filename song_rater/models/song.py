from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title} (by {self.artist})'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'artist'], name='unique_song')
        ]


class Rating(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                          MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)
