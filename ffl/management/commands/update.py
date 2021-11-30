from django.core.management.base import BaseCommand
from nfldfs import games as games
from ...models import Player, PlayerWeek, Pick
from ...settings import CURRENT_SEASON, get_week


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('season', type=int, nargs="?",
                            default=CURRENT_SEASON, help="Current season of NFL")
        parser.add_argument(
            'week', type=int, nargs="?", default=get_week()-1, help="Current week of NFL season")

    def handle(self, *args, **kwargs):
        season = kwargs['season']
        week = kwargs['week']
        self.stdout.write(f"Season: {season}, Week: {week}")

        self.update_players(week, season)
        self.update_picks(week, season)

    def update_players(self, week, season):

        g = games.find_games('yh', season, week)
        stats = games.get_game_data(g)

        for row in stats.itertuples():
            player, created = Player.objects.get_or_create(
                id=row.Index, defaults={
                    "name": row.player_name,
                    "position": row.position,
                    "team": row.team_name
                }
            )

            player_week, created = PlayerWeek.objects.update_or_create(
                player=player,
                week=week,
                season=season,
                defaults={
                    "points": row.points
                }
            )

    def update_picks(self, week, season):
        picks = Pick.objects.filter(week=week, season=season)

        for pick in picks:
            try:
                qb = Player.objects.get(id=pick.qb_id).weeks.get(
                    week=week, season=season)
                pick.qb_points = qb.points
            except PlayerWeek.DoesNotExist:
                pick.qb_points = 0
            except Player.DoesNotExist:
                print(pick)
            try:
                rb = Player.objects.get(id=pick.rb_id).weeks.get(
                    week=week, season=season)
                pick.rb_points = rb.points
            except PlayerWeek.DoesNotExist:
                pick.rb_points = 0
            except Player.DoesNotExist:
                print(pick)
            try:
                wr = Player.objects.get(id=pick.wr_id).weeks.get(
                    week=week, season=season)
                pick.wr_points = wr.points
            except PlayerWeek.DoesNotExist:
                pick.wr_points = 0
            except Player.DoesNotExist:
                print(pick)
            try:
                te = Player.objects.get(id=pick.te_id).weeks.get(
                    week=week, season=season)
                pick.te_points = te.points
            except PlayerWeek.DoesNotExist:
                pick.te_points = 0
            except Player.DoesNotExist:
                print(pick)
            try:
                defense = Player.objects.get(id=pick.defense_id).weeks.get(
                    week=week, season=season)
                pick.def_points = defense.points
            except PlayerWeek.DoesNotExist:
                pick.def_points = 0
            except Player.DoesNotExist:
                print(pick)
            pick.save()
