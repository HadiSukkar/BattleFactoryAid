from django.urls import path
from . import views

urlpatterns = [
    path('team-search/', views.teams_search_view, name='team_search')
]