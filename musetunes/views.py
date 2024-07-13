from django.shortcuts import render
from fairytones.models import Song
from fairytones.models import Playlist
from django.db.models import Case, When
from django.contrib.auth.models import User

def index(request):
    song = Song.objects.all()[:25]
    watch = []

    if request.user.is_authenticated:
        wl = Playlist.objects.filter(user=request.user)
        ids = [i.video_id for i in wl if i.video_id]
        if ids:
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
            watch = Song.objects.filter(song_id__in=ids).order_by(preserved)
            watch = reversed(watch)
        else:
            watch = Song.objects.all()[:25]
    else:
        watch = Song.objects.all()[:25]

    return render(request, 'index.html', {'song': song, 'watch': watch})