from rest_framework import routers
from .views import LeagueViewSet, JoinLeagueView, PickView, PlayerViewSet, WeekView, TeamViewSet, LeagueWeeksView, ACPlayerViewSet
from django.urls import path

router = routers.DefaultRouter()
router.register('league', LeagueViewSet, basename="league")

player_list = PlayerViewSet.as_view({'get': 'list'})
player_detail = PlayerViewSet.as_view({'get': 'retrieve'})
team_list = TeamViewSet.as_view({'get': 'list'})
autocomplete_players = ACPlayerViewSet.as_view({"get": "list"})

urlpatterns = [
    path('join', JoinLeagueView.as_view()),
    path('pick/<int:pk>', PickView.as_view()),
    path('players', player_list),
    path('autocomplete', autocomplete_players),
    path('players/<str:id>', player_detail),
    path('week', WeekView.as_view()),
    path('team', team_list),
    path('league/weeks', LeagueWeeksView.as_view())
]

urlpatterns += router.urls
