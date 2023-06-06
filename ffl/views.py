from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import viewsets, views, permissions
from rest_framework import status
from .models import League, FantasyTeam, Pick, Player, Team
from .serializers import LeagueDetailSerializer, LeagueSerializer, CreateLeagueSerializer, PickSerializer, PlayerDetailSerializer, PlayerSerializer, TeamSerializer
from rest_framework.response import Response
from .settings import get_week


# Create your views here.

class LeagueWeeksView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        week = get_week()
        league_id = request.query_params.get("leagueId")
        league = League.objects.get(pk=league_id)
        picks = Pick.objects.filter(team__league=league, week__lt=week)
        data = PickSerializer(picks, many=True)
        
        return Response(data.data)


class JoinLeagueView(views.APIView):

    def post(self, request, *args, **kwargs):
        """
            NOT DONE
        """
        user = request.user
        try:
            league = League.objects.get(name=request.data['league'])

        except:
            return Response({'error': f"No League by the name of {request.data['league']}"})

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
    permission_classes= [permissions.AllowAny] # TURN OFF IN PRODUCTION

    def get_object(self, pk=None):
        return Pick.objects.get(pk=pk)

    def patch(self, request, *args, **kwargs):
        pick = self.get_object(pk=kwargs.get('pk'))

        week = pick.week
        season = pick.season

        # Quarterback
        qb_id = request.data.get('qb_id', '')
        if qb_id:
            qb_week = Player.objects.get(pk=qb_id).weeks.get_or_create(week=week, season=season)[0]
            qb_week.save()
            pick.qb = qb_week
            pick.save()

        # Running Back
        rb_id = request.data.get('rb_id', '')
        if rb_id:
            rb_week = Player.objects.get(pk=rb_id).weeks.get_or_create(week=week, season=season)[0]
            rb_week.save()
            pick.rb = rb_week
            pick.save()

        # Wide Receiver
        wr_id = request.data.get('wr_id', '')
        if wr_id:
            wr_week = Player.objects.get(pk=wr_id).weeks.get_or_create(week=week, season=season)[0]
            wr_week.save()
            pick.wr =wr_week
            pick.save()

        # Tight End 
        te_id = request.data.get('te_id', '')
        if te_id:
            te_week = Player.objects.get(pk=te_id).weeks.get_or_create(week=week, season=season)[0]
            te_week.save()
            pick.te = te_week
            pick.save()

        # Defense
        defense_id = request.data.get('defense_id', '')
        if defense_id:
            defense_week = Team.objects.get(pk=defense_id).defenses.get_or_create(week=week, season=season)[0]
            defense_week.save()
            pick.defense = defense_week
            pick.save()
        
        
        #return Response(PickSerializer(pick).data, status=status.HTTP_200_OK)
        serializer = PickSerializer(pick, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            print("serializer: ", serializer.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print("serializer errors", serializer.errors)
        #return Response(serializer.errors)

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"
    pagination_class = None

    def list(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"
    pagination_class = None

    def retrieve(self, request, id=None):
        player = get_object_or_404(self.queryset, pk=id)
        serializer = PlayerDetailSerializer(player)
        return Response(serializer.data)


class WeekView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        week = get_week()
        return Response({
            "week": week
        })
