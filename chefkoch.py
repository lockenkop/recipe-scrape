from os import name
import re
import sqlite3
import time
from sqlite3.dbapi2 import Time

from recipe_scrapers import scrape_me

class recipeScraper():
    def __init__(self) -> None:
        pass
        self.con = sqlite3.connect('recipes.db')
        self.cur = self.con.cursor()
        self.URL = "https://www.chefkoch.de/rezepte/zufallsrezept/"

    def search_ingred(self, ingreds_to_search):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

        table_names = self.cur.fetchall()
        for table_name in table_names:
            ingreds_matching = 0
            for ingred in ingreds_to_search:
                querry = "SELECT url FROM '{}' WHERE ingred LIKE '%{}%'".format(table_name[0], ingred)
                self.cur.execute(querry)
                result = self.cur.fetchone()
                if result: ingreds_matching += 1
            if ingreds_matching == len(ingreds_to_search):
                print(f"Gefunden {result}")
            
    
    def table_exists(self, name):
        querry = f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{name}'"
        return self.cur.execute(querry).fetchone() is not None

    def scrapeRecipe(self, amount, url=None):
        
        if url is None:
            scraper = scrape_me(self.URL)
        elif url:
            scraper = scrape_me(url)
            amount = 1
        if amount == "inf":
            while True:
                try:
                    self.scrapeRecipe(1)
                except:
                    print("Hupala")
        recipe_url = scraper.canonical_url()
        title = scraper.title()
        char_to_remove = ["-", "\"", "\'"]
        for char in char_to_remove:
            title = title.replace(char, "")
        ingreds = scraper.ingredients()
        yields = scraper.yields()
        print(f"adding {title}")
        
        if not self.table_exists(title):
            self.cur.execute("CREATE TABLE '{}' (ingred text, url text)".format(title))
        for ingred in ingreds:
            self.cur.execute(" insert into '{}' values (?, ?)".format(title), (ingred, recipe_url))
        self.con.commit()
        time.sleep(0.4)