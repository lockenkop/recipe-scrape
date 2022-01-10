"""
chefkoch recipe scraper and databank
"""

import platform
import sqlite3

os_name = platform.platform()
if "arm" not in os_name:
    from recipe_scrapers import scrape_me
else:
    print("this system cannot scrape recipes")
class RecipeScraper():
    def __init__(self) -> None:
        self.con = sqlite3.connect('recipes.db')
        self.cur = self.con.cursor()
        self.URL = "https://www.chefkoch.de/rezepte/zufallsrezept/"

    def search_ingred(self, ingreds_to_search):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

        table_names = self.cur.fetchall()
        links = []
        for table_name in table_names:
            ingreds_matching = 0
            for ingred in ingreds_to_search:
                querry = "SELECT recipe_url, image_url FROM '{}' WHERE ingred LIKE '%{}%'".format(table_name[0], ingred)
                self.cur.execute(querry)
                result = self.cur.fetchone()
                if result: ingreds_matching += 1
            if ingreds_matching == len(ingreds_to_search):
                links.append(result)
        return links

    def table_exists(self, name):
        querry = f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{name}'"
        return self.cur.execute(querry).fetchone() is not None

    def showRecipe(self, name):
        found_tables = []
        found_recipes = []

        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

        tables = self.cur.fetchall()
        for table in tables:
            if name in table[0]:
                found_tables.append(table)
        for name in found_tables:
            print(name)
            querry = f"SELECT recipe_url, image_url FROM '{name[0]}'"
            print(querry)
            self.cur.execute(querry)
            recipe = self.cur.fetchone()
            found_recipes.append(recipe)
        return found_recipes

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
                except RuntimeError:
                    print("Hupala")
        recipe_url = scraper.canonical_url()
        title = scraper.title()
        image_url = scraper.image()
        # yields = scraper.yields()
        char_to_remove = ["-", "\"", "\'"]
        for char in char_to_remove:
            title = title.replace(char, "")
        ingreds = scraper.ingredients()
        
        if not self.table_exists(title):
            print(f"adding {title}")
            self.cur.execute("CREATE TABLE '{}' (ingred text, recipe_url text, image_url text)".format(title))
            for ingred in ingreds:
                self.cur.execute(" insert into '{}' values (?, ?, ?)".format(title), (ingred, recipe_url, image_url))
        else:
            print("recipe already exists")
        self.con.commit()
