from django.shortcuts import render, redirect
from django.db.models import Case, When
from fairytones.models import Song, Playlist,History
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count

def search(request):
    query = request.GET.get("query")
    if query:
        songs = Song.objects.filter(name__icontains=query)
    else:
        songs = Song.objects.none() 
    return render(request, 'fairytones/search.html', {"songs": songs, "query": query})




def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()

        return redirect(f"/fairytones/songs/{music_id}")

    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, 'fairytones/history.html', {"history": song})
def playlist(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST.get('video_id', None)

        if video_id:
            # Check if the video_id is already in the playlist
            if Playlist.objects.filter(user=user, video_id=video_id).exists():
                message = "Your Video is Already Added"
            else:
                # Ensure video_id exists in Song model
                song = Song.objects.filter(song_id=video_id).first()
                if song:
                    new_playlist = Playlist(user=user, video_id=video_id)
                    new_playlist.save()
                    message = "Your Video is Successfully Added"
                else:
                    message = "Invalid video ID"
        else:
            message = "Invalid video ID"
        
        # Retrieve the updated playlist songs
        songs = get_user_playlist(request.user)
        
        # Render the playlist page with the updated message and playlist
        return render(request, "fairytones/playlist.html", {'songs': songs, 'message': message})
    
    # GET request handling for displaying existing playlist
    songs = get_user_playlist(request.user)
    return render(request, "fairytones/playlist.html", {'songs': songs})

def get_user_playlist(user):
    # Retrieve the user's playlist and order songs by their position in the playlist
    wl = Playlist.objects.filter(user=user)
    ids = [i.video_id for i in wl if i.video_id]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    songs = Song.objects.filter(song_id__in=ids).order_by(preserved)
    return songs




def index(request):
    song = Song.objects.all()
    watch = []

    if request.user.is_authenticated:
        wl = Playlist.objects.filter(user=request.user)
        ids = [i.video_id for i in wl if i.video_id]

        if ids:
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
            watch = Song.objects.filter(song_id__in=ids).order_by(preserved)
            watch = list(reversed(watch))
        else:
            watch = Song.objects.all()[:3]
    else:
        watch = Song.objects.all()[:3]

    return render(request, 'index.html', {'song': song, 'watch': watch})

def songs(request):
    song = Song.objects.all()
    return render(request, 'fairytones/songs.html', {'song': song})

def songpost(request, id):
    song = Song.objects.filter(song_id=id).first()
    return render(request, 'fairytones/songpost.html', {'song': song})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
    return render(request, 'fairytones/login.html')

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()
            user = authenticate(username=username, password=pass1)
            if user:
                login(request, user)
                return redirect('/')
    return render(request, 'fairytones/signup.html')

def logout_user(request):
    logout(request)
    return redirect("/")
