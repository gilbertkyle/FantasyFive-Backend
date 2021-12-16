from rest_framework import serializers
from .models import Pick, League, FantasyTeam, Player, User
from accounts.serializers import UserSerializer


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


class PickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pick
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    picks = PickSerializer(many=True)

    class Meta:
        model = FantasyTeam
        fields = ['pk', 'name', 'owner', 'picks']
        depth = 2


class LeagueDetailSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True)
    admins = UserSerializer(many=True)

    class Meta:
        model = League
        fields = ['pk', 'name', 'teams', 'admins']
        depth = 2


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = '__all__'
