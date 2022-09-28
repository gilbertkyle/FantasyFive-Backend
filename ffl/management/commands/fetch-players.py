from django.core.management.base import BaseCommand
from ...models import Player, PlayerWeek, Pick
from ...settings import CURRENT_SEASON, get_week
from selenium.webdriver.common.by import By

from selenium import webdriver


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        browser = webdriver.Chrome(options=chrome_options)
        try:
            browser.get("https://fantasy.espn.com/football/leaders")
            print("Page title was '{}'".format(browser.title))
            elem = browser.find_element(By.CLASS_NAME, "players-table")
            print(elem)
        finally:
            browser.quit()
