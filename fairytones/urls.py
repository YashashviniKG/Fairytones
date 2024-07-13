from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('songs/', views.songs, name='songs'),
    path('songs/<int:id>', views.songpost, name='songpost'),
    path('login', views.login_user, name='login'),
    path('signup', views.signup, name='signup'),
    path('playlist', views.playlist, name='playlist'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('history', views.history, name='history'),
    path('search', views.search, name='searc')
]
