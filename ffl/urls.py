from rest_framework import routers
from .views import LeagueViewSet, JoinLeagueView, PickView, PlayerViewSet, WeekView
from django.urls import path

router = routers.DefaultRouter()
router.register('league', LeagueViewSet, basename="league")

player_list = PlayerViewSet.as_view({'get': 'list'})
player_detail = PlayerViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('join', JoinLeagueView.as_view()),
    path('pick/<int:pk>', PickView.as_view()),
    path('player', player_list),
    path('player/<str:id>', player_detail),
    path('week', WeekView.as_view())
]

urlpatterns += router.urls
