from turtle import position
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from ...settings import CURRENT_SEASON, get_week
from ...models import Player, PlayerWeek
import nfl_data_py as nfl

class Command(BaseCommand):

  def add_arguments(self, parser):
      parser.add_argument('season', type=int, nargs="?",
                            default=CURRENT_SEASON, help="Current season of NFL")
      parser.add_argument(
            'week', type=int, nargs="?", default=get_week()-1, help="Current week of NFL season")


  def fetch_defenses(self, *args, **kwargs):
    defenses = nfl.import_team_desc()
    for row, index in defenses.iterrows():
      continue

  def handle(self, *args, **kwargs):
        season = kwargs["season"]
        week = kwargs["week"]
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        browser = webdriver.Chrome(options=chrome_options)
        
        try:
            browser.get("https://football.fantasysports.yahoo.com/f1/528/players?&sort=AR&sdir=1&status=ALL&pos=DEF&stat1=S_W_3&jsenabled=1")
            print("Page title was '{}'".format(browser.title))
            table = browser.find_element(By.ID, "players-table").find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, 'tbody')
            count = 0
            button = browser.find_element(By.CLASS_NAME, 'navlist').find_element(By.TAG_NAME, 'a') 
            for row in table.find_elements(By.TAG_NAME, "tr"):
              defense = {}
              points = row.find_element(By.CLASS_NAME, 'pts')
              player = row.find_element(By.CLASS_NAME, 'player')
              team_name_full = player.find_element(By.CLASS_NAME, 'name')
              team_name = team_name_full.find_element(By.XPATH, "following-sibling::*[1]")
              defense["points"] = points.text
              defense["team_full"] = team_name_full.text
              defense["team"] = team_name.text.split()[0]

              print(defense)

              new_player, created = Player.objects.get_or_create(
                name=defense["team"], defaults={
                  "position": "DEF"
                }
              )

              player_week = PlayerWeek.objects.get_or_create(
                player=new_player, 
                week=week,
                season=season,
                
                defaults={
                  "points": defense["points"]
                }
              )

        finally:
            browser.quit()

    