from django.core.management.base import BaseCommand
import nfl_data_py as nfl
from ...models import Team


class Command(BaseCommand):

  def fetch_defenses(self, *args, **kwargs):
    teams = nfl.import_team_desc()
    defunct_teams = ["LAR", "SD", "OAK", "STL"]
    for index, team in teams.iterrows():
      if team.team_abbr in defunct_teams:
        continue
      new_team, created = Team.objects.get_or_create(
        team_id=team.team_id, defaults={
          "team_abbr": team.team_abbr,
          "team_name": team.team_name,
          "team_color": team.team_color,
          "team_color2": team.team_color2,
          "team_color3": team.team_color3,
          "team_color4": team.team_color4,
          "team_logo": team.team_logo_wikipedia
        }
      )  

  def handle(self, *args, **kwargs):
    self.fetch_defenses()