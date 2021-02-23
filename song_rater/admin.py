from django.contrib import admin
from .models import Song, Rating


class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist',)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('song', 'rating',)


admin.site.register(Song, SongAdmin)
admin.site.register(Rating, RatingAdmin)
