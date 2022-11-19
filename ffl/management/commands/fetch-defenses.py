from click import option
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from ...settings import CURRENT_SEASON, get_week
from ...models import Player, PlayerWeek, Team, Defense
import nfl_data_py as nfl
from decimal import Decimal
from webdriver_manager.chrome import ChromeDriverManager
import os

class Command(BaseCommand):

  def add_arguments(self, parser):
      parser.add_argument('season', type=int, nargs="?",
                            default=CURRENT_SEASON, help="Current season of NFL")
      parser.add_argument(
            'week', type=int, nargs="?", default=get_week()-2, help="Current week of NFL season")

  def scrape_table(self, table, season, week, *args, **kwargs):
    print("length: ", len(table.find_elements(By.TAG_NAME, "tr")))
    for row in table.find_elements(By.TAG_NAME, "tr"):
      try:
        defense = {}
        points = row.find_element(By.CLASS_NAME, 'pts')
        player = row.find_element(By.CLASS_NAME, 'player')
        team_name_full = player.find_element(By.CLASS_NAME, 'name')
        team_name = team_name_full.find_element(By.XPATH, "following-sibling::*[1]")
        try:
          defense["points"] = Decimal(points.text)
        except:
          defense["points"] = Decimal(0.0)
          print(f"No points for {team_name_full}")
        defense["team_full"] = team_name_full.text
        defense["team"] = team_name.text.split()[0].upper()

        print(defense)

        try:
          # check if defense already exists
          dst = Defense.objects.update_or_create(team__team_abbr=defense["team"], season=season, week=week, defaults={
            "fantasy_points": defense["points"]
          })
        except:
          # if defense doesn't exist
          team = Team.objects.filter(team_abbr=defense["team"]).first()
          if team is None:
            print("fail: ", defense)
            continue
          dst = Defense.objects.update_or_create(team=team, week=week, season=season, fantasy_points=defense["points"])
      except:
        print("some sort of error???")



  def handle(self, *args, **kwargs):
        season = kwargs["season"]
        week = kwargs["week"]
        chrome_options = webdriver.ChromeOptions()
        chromedriver_version = os.getenv("CHROMEDRIVER_VERSION", "107.0.5304.62")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        if os.getenv("CHROMEDRIVER_VERSION"):
          browser  = webdriver.Chrome(options=chrome_options)   
        else:
          browser = webdriver.Chrome(ChromeDriverManager(version=chromedriver_version).install(), options=chrome_options)
        #browser = webdriver.Chrome(ChromeDriverManager(version=chromedriver_version).install(), options=chrome_options)

        url1 = f"https://football.fantasysports.yahoo.com/f1/528/players?&sort=AR&sdir=1&status=ALL&pos=DEF&stat1=S_W_{week}&jsenabled=1"
        url2 = f"https://football.fantasysports.yahoo.com/f1/528/players?status=ALL&pos=DEF&cut_type=9&stat1=S_W_{week}&myteam=0&sort=AR&sdir=1&count=25"

        try:

            browser.get(url1)
            print("Page title was '{}'".format(browser.title))

            table = browser.find_element(By.ID, "players-table").find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, 'tbody')

            #button = browser.find_element(By.CLASS_NAME, 'navlist').find_element(By.TAG_NAME, 'a')
            self.scrape_table(table, season, week)

            browser.get(url2)
            table = browser.find_element(By.ID, "players-table").find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, 'tbody')
            self.scrape_table(table, season, week)

        finally:
            browser.quit()

