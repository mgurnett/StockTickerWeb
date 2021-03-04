from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('teams', views.teams_view, name = "teams"),    
    path('players', views.players_view, name = "players"), 
]
