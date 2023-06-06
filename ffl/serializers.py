from rest_framework import serializers
from .models import Pick, League, FantasyTeam, Player, PlayerWeek, Team, User, Defense
from accounts.serializers import UserSerializer
from .settings import CURRENT_SEASON


class FantasyTeamSerializer2(serializers.ModelSerializer):
    owner = UserSerializer()
    
    class Meta:
        model = FantasyTeam
        fields = ['pk', 'name', 'owner', 'picks']
        depth = 3

class DefenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Defense
        fields = '__all__'
        depth = 2

class PlayerWeekSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerWeek
        fields = '__all__'
        depth = 2

class CreateLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['name', 'password']


class RegisterLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['name', 'password']


class LeagueSerializer(serializers.ModelSerializer):
    admins = UserSerializer(many=True)

    class Meta:
        model = League
        fields = ['pk', 'name', 'password', 'admins']
        extra_kwargs = {'password': {'write_only': True}}


class RecentPickSerializer(serializers.ListSerializer):
    """
    Serializer that only returns picks from the current season
    """
    def to_representation(self, data):
        data = data.filter(season=CURRENT_SEASON)
        return super(RecentPickSerializer, self).to_representation(data)

class PickSerializer(serializers.ModelSerializer):
    qb = PlayerWeekSerializer()
    rb = PlayerWeekSerializer()
    wr = PlayerWeekSerializer()
    te = PlayerWeekSerializer()
    defense = DefenseSerializer()
    team = FantasyTeamSerializer2()


    class Meta:
        model = Pick
        fields = '__all__'
        list_serializer_class = RecentPickSerializer

class FantasyTeamSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    picks = PickSerializer(many=True)

    class Meta:
        model = FantasyTeam
        fields = ['pk', 'name', 'owner', 'picks']
        depth = 3

class LeagueDetailSerializer(serializers.ModelSerializer):
    teams = FantasyTeamSerializer(many=True)
    admins = UserSerializer(many=True)

    class Meta:
        model = League
        fields = ['pk', 'name', 'teams', 'admins']
        depth = 2

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = "__all__"

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Player
        fields = '__all__'



class PlayerDetailSerializer(serializers.ModelSerializer):
    weeks = PlayerWeekSerializer(many=True)

    class Meta:
        model = Player
        fields = '__all__'


