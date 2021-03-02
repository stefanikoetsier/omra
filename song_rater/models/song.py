from django.db import models


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

    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )

    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
