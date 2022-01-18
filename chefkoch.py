"""
chefkoch recipe scraper and databank
"""

from msilib.schema import Error
import platform
import sqlite3
from germalemma import GermaLemma

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
        self.lemma = GermaLemma()
        self.nonVegetarisch = [
            "Fleisch",
            "Keule",
            "Fisch",
            "Hähnchenkeule"
        ]
        self.nonVegan = [
            "Ei",
            "Honig",            
        ]

    def lemmantizer(self, ingreds):
        ingreds_lemmantized = []
        for ingred in ingreds:
            ingred = ingred.capitalize()
            ingreds_lemmantized.append(self.lemma.find_lemma(ingred,"N"))
        return ingreds_lemmantized

    def search_ingred(self, ingreds_to_search, mode):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = self.cur.fetchall()
        links = []
        ingreds_to_search = self.lemmantizer(ingreds_to_search)
        print(ingreds_to_search)
        for table_name in table_names:
            try:
                ingreds_matching = 0
                check = 0
                check = self.check_vegan(table_name[0], mode)
                if check:
                    print("not vegan rejecting recipe")
                    continue
                for ingred in ingreds_to_search:
                    querry = "SELECT recipe_url, image_url FROM '{}' WHERE ingred LIKE '%{}%'".format(table_name[0], ingred)
                    self.cur.execute(querry)
                    result = self.cur.fetchone()
                    if result: ingreds_matching += 1
                if ingreds_matching == len(ingreds_to_search):
                    links.append(result)
            except:
                return "das hat nciht funtioniert"
        return links

    def recipe_amount(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cur.fetchall()
        amount = len(tables)
        return amount

    def table_exists(self, name):
        querry = f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{name}'"
        return self.cur.execute(querry).fetchone() is not None

    def check_vegan(self, table, mode):
        querry_for_all_ingreds = "SELECT ingred FROM '{}'".format(table)
        self.cur.execute(querry_for_all_ingreds)
        ingreds_in_recipe = self.cur.fetchall()

        for ingred in ingreds_in_recipe:
            ingred_words = ingred[0].split()
            for ingred_word in ingred_words:             
                if mode == 1:
                    if ingred_word in self.nonVegetarisch:
                        print(f"{ingred} not vegetarian")
                        return 1
                elif mode == 2:
                    if ingred_word in self.nonVegan:
                        print(f"{ingred} not vegan")
                        return 1
        else:
            return 0

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
                    print("going again")
                    self.scrapeRecipe(1)
                except RuntimeError:
                    print("Hupala")
        recipe_url = scraper.canonical_url()
        title = scraper.title()
        image_url = scraper.image()
        char_to_remove = ["-", "\"", "\'"]
        for char in char_to_remove:
            title = title.replace(char, "")
        ingreds = scraper.ingredients()
        
        if not self.table_exists(title):
            try:
                print(f"adding {title}")
                self.cur.execute("CREATE TABLE '{}' (ingred text, recipe_url text, image_url text)".format(title))
            except:
                print("Mousse au chocolat du Wichser!")
            for ingred in ingreds:
                self.cur.execute(" insert into '{}' values (?, ?, ?)".format(title), (ingred, recipe_url, image_url))
        else:
            print("recipe already exists")
        self.con.commit()
