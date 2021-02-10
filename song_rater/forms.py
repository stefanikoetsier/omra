from django import forms


class AddSongForm(forms.Form):
    artist = forms.CharField(label='artist', max_length=100)
    title = forms.CharField(label='title', max_length=100)
