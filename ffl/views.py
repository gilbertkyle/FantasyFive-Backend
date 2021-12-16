from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import generics, serializers, viewsets, views, permissions
from rest_framework import status
from .models import League, FantasyTeam, Pick, Player
from .serializers import LeagueDetailSerializer, LeagueSerializer, CreateLeagueSerializer, PickSerializer, PlayerSerializer
from rest_framework.response import Response
from .settings import get_week
import datetime


# Create your views here.


class JoinLeagueView(views.APIView):

    def post(self, request, *args, **kwargs):
        """
            NOT DONE
        """
        user = request.user
        try:
            league = League.objects.get(name=request.data['name'])

        except:
            return Response({'error': f"No League by the name of {request.data['name']}"})

        if check_password(request.data['password'], league.password):
            league.add_team(user)
        else:
            return Response({'error': 'Password does not match'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "league": LeagueSerializer(league).data
        })


class LeagueViewSet(viewsets.ModelViewSet):

    def get_object(self):
        league = League.objects.get(pk=self.kwargs['pk'])
        return league

    def get_queryset(self):
        user = self.request.user
        return League.objects.filter(teams__owner=user).distinct()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve":
            return LeagueDetailSerializer
        return LeagueSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        league = self.get_object()
        serializer = LeagueDetailSerializer(league)
        return Response(serializer.data)

    def list(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        print(request.data)
        serializer = CreateLeagueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        league = League.objects.create_league(
            serializer.data['name'], serializer.data['password'], user)

        # create new team and assign to user
        league.add_team(user)

        return Response({
            "league": LeagueSerializer(league, context=self.get_serializer_context()).data
        })

    def destroy(self, request, pk=None):
        pass


class PickView(views.APIView):
    def get_object(self, pk=None):
        return Pick.objects.get(pk=pk)

    def patch(self, request, *args, **kwargs):
        print("got here")
        pick = self.get_object(pk=kwargs.get('pk'))
        serializer = PickSerializer(pick, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors)


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    permission_classes = [permissions.AllowAny]


class WeekView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        week = get_week()
        return Response({
            "week": week
        })
