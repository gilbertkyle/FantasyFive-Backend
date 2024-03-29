from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .settings import CURRENT_SEASON, NUMBER_OF_WEEKS
import datetime

User = get_user_model()

# Create your models here.


class LeagueManager(models.Manager):
    def create_league(self, name, password, user):

        hashed_password = make_password(password)
        league = self.create(name=name, password=hashed_password)
        league.admins.add(user)
        league.save()

        # add team to league
        league.add_team(user)

        return league


class TeamManager(models.Manager):
    def create_team(self, user):
        team = self.create()
        team.owner = user
        team.save()
        return team


class Defense(models.Model):
    team = models.ForeignKey("Team",to_field="team_id", related_name="defenses", on_delete=models.CASCADE)
    week = models.IntegerField("Week")
    season = models.IntegerField("Season", default=CURRENT_SEASON)
    fantasy_points = models.FloatField("Fantasy Points", default=0.0)

    def __str__(self) -> str:
        return f"{self.team.team_name} Week {self.week} year {self.season}"


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    team_abbr = models.CharField("Team Name Abbreviation", default="", max_length=5, null=False, blank=False)
    team_name = models.CharField("Team Name", default="", max_length=30, null=False, blank=False)
    team_color = models.CharField("Primary Color", default="", max_length=10)
    team_color2 = models.CharField("Secondary Color", default="", max_length=10)
    team_color3 = models.CharField("Tertiary Color", default="", max_length=10)
    team_color4 = models.CharField("Quaternary Color", default="", max_length=10)
    team_logo = models.CharField("Team Logo", default="", max_length=250)

    def __str__(self) -> str:
        return f"{self.team_name}"


class Pick(models.Model):
    team = models.ForeignKey(
        "FantasyTeam", on_delete=models.SET_NULL, related_name="picks", null=True)

    week = models.IntegerField()
    season = models.IntegerField(default=datetime.datetime.now().year)

    qb = models.ForeignKey("PlayerWeek", on_delete=models.SET_NULL, related_name="quarterback", null=True, blank=True)
    rb = models.ForeignKey("PlayerWeek", on_delete=models.SET_NULL, related_name="running_back", null=True)
    wr = models.ForeignKey("PlayerWeek", on_delete=models.SET_NULL, related_name="wide_receiver", null=True)
    te = models.ForeignKey("PlayerWeek", on_delete=models.SET_NULL, related_name="tight_end", null=True)
    defense = models.ForeignKey("Defense", on_delete=models.SET_NULL, related_name="defense", null=True)

    pick_time = models.DateTimeField('Date Picked', auto_now_add=True)

    def __str__(self):
        return f"{self.team}, Week {self.week}"

    def total_points(self, *args, **kwargs):
        return (
            self.qb.points +
            self.rb.points +
            self.wr.points +
            self.te.points +
            self.defense.points
        )

    """ def save(self, *args, **kwargs):
        self.total_points = (
            self.qb_points +
            self.rb_points +
            self.wr_points +
            self.te_points +
            self.defense_points
        )
        super(Pick, self).save(*args, **kwargs) """


class League(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=150, null=False)
    admins = models.ManyToManyField(User, related_name="admins")
    objects = LeagueManager()

    def __str__(self) -> str:
        return self.name

    def create_new_season(self):
        for team in self.teams.all():
            team._create_picks()

    def add_team(self, user):
        if user in [team.owner for team in self.teams.all()]:
            return
        team = FantasyTeam()
        team.owner = user
        team.league = self
        team.save()
        team.name = user.username
        team.save()
        team._create_picks()
        return team


class FantasyTeam(models.Model):
    name = models.CharField(max_length=50, default="default name")
    owner = models.ForeignKey(
        User, related_name="owner", on_delete=models.SET_NULL, null=True)
    league = models.ForeignKey(
        League, on_delete=models.CASCADE, related_name="teams")
    objects = TeamManager()

    def _create_picks(self, season=CURRENT_SEASON):

        for week in range(1, NUMBER_OF_WEEKS+1):
            pick, created = Pick.objects.get_or_create(
                week=week, season=season, team=self)
            if created:
                pick.team = self
                pick.save()

    def __str__(self, *args, **kwargs) -> str:
        return f"{self.name}"


class Player(models.Model):
    id = models.CharField('id', max_length=20,
                          unique=True, primary_key=True)
    name = models.CharField('Name', max_length=30)
    position = models.CharField('Position', max_length=5, default="")
    team = models.ForeignKey(Team, to_field="team_id", related_name="players", on_delete=models.CASCADE, default=0) 

    def __str__(self):
        return self.name


class PlayerWeek(models.Model):
    player = models.ForeignKey(
        Player, to_field="id", on_delete=models.CASCADE, related_name="weeks", null=False)
    season = models.IntegerField("Season", default=CURRENT_SEASON)
    week = models.IntegerField("Week")
    points = models.FloatField("Points", default=0.0)

    # these fields not in use as of 9/1/2020, but won't be deleted in case I use them later
    passing_yds = models.IntegerField("Passing Yards", default=0)
    passing_tds = models.IntegerField("Passing Touchdowns", default=0)
    passing_ints = models.IntegerField("Passing Interceptions", default=0)
    rushing_yds = models.IntegerField("Rushing Yards", default=0)
    rushing_tds = models.IntegerField("Rushing Touchdowns", default=0)
    receiving_yds = models.IntegerField("Receiving Yards", default=0)
    receiving_tds = models.IntegerField("Receiving Touchdowns", default=0)
    kick_ret_tds = models.IntegerField("Kick Return Touchdowns", default=0)
    two_point_conversions = models.IntegerField(
        "Two Point Conversions", default=0)
    fumbles_lost = models.IntegerField("Fumbles Lost", default=0)
    fumbles_rec_tds = models.IntegerField(
        "Fumble Recovery Touchdowns", default=0)

    def __str__(self):
        return f"{self.player.name}, week {self.week}, {self.season}"
