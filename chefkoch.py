"""
chefkoch recipe scraper and databank
"""

import platform
import sqlite3
from germalemma import GermaLemma
import logging
import datetime

from numpy import add_docstring

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

        date = datetime.date.today()

        self.logging_level="DEBUG"

        logging.basicConfig(filename=f'{date.year}-{date.month}-{date.year}.log', level=logging.DEBUG)
        
        
        self.nonVegetarisch = [
            "Fleisch",
            "Keule",
            "Fisch",
            "Hähnchenkeule",
            "Rind",
            "Hackfleisch",
            "Schwein",
            "Kalb",
            "Leber",
            "Niere",
            "Entrecôte",
            "Kasseler",
            "Kassler",
            "Bacon",
            "Huhn",
            "Hühnerbrust",
            "Hühnerbrüste",
            "Cabanossi"
        ]
        self.nonVegan = [
            "Ei",
            "Honig",
            "Butter",
            "Ei(er)"
        ]
        self.vegetarianAlternatives = [
            "vegetarisch",
            "vegetarian"    
        ]
        self.veganAlternatives = [
            "vegan"
            "Margarine",
            ""
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
        print(f"searching for: {ingreds_to_search}")
        for table_name in table_names:
            try:
                ingreds_matching = 0
                
                if mode > 0:
                    if self.check_vegan(table_name, mode):
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
                return [["//////wrong return value","check code"]]
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
        not_vegetarian = 0
        not_vegan = 0
        has_alternative = 0
        
        querry_for_all_ingreds = "SELECT ingred FROM '{}'".format(table[0])
        self.cur.execute(querry_for_all_ingreds)
        ingreds_in_recipe = self.cur.fetchall()
        

        for ingred in ingreds_in_recipe:
            ingred_words = ingred[0].split()
            
            for ingred_word in ingred_words:             
                if mode >= 1:
                    for nonVegetarisch  in self.nonVegetarisch: 
                        not_vegetarian = nonVegetarisch in ingred_word
                        if not_vegetarian:
                            print(f"{ingred_word} not vegetarian")
                            for ingred_word in ingred_words:
                                for vegetarianAlternative in self.vegetarianAlternatives:
                                    has_alternative = vegetarianAlternative in ingred_word
                                    if has_alternative:
                                        print(f"{ingred} has alternative")
                            return 1
                        
                    
                    
                    

                elif mode == 2:
                    not_vegan = ingred_word in self.nonVegan or ingred_word in self.nonVegetarisch
                    has_alternative = ingred_word in self.veganAlternatives
                if  not_vegan and not has_alternative:
                    print(f"{ingred} not vegan, or vegetarian")
                    return 1
        else:
            return 0

    def showRecipe(self, name, mode):
        found_tables = []
        found_recipes = []

        querry_for_all_tables = "SELECT name FROM sqlite_master WHERE type='table'" 
        self.cur.execute(querry_for_all_tables)
        tables = self.cur.fetchall()

        for table in tables:
            if name in table[0]:
                found_tables.append(table)
        for name in found_tables:
            # print(name)
            querry = f"SELECT recipe_url, image_url FROM '{name[0]}'"
            # print(querry)
            self.cur.execute(querry)
            recipe = self.cur.fetchone()
            if not self.check_vegan(name, mode):
                found_recipes.append(recipe)
        if isinstance(found_recipes, list):
            return found_recipes
        else:
            if self.logging_level == "DEBUG": logging.debug("foundrecipes didnt return list")
            return [["//////wrong return value","check code"]]


    def scrapeRecipe(self, amount, url=None):
        if url is None:
            scraper = scrape_me(self.URL)
        elif url:
            scraper = scrape_me(url)
            amount = 1
        if amount == "inf":
            if self.logging_level == "DEBUG": logging.debug("starting infinite scrape")
            while True:
                try:
                    self.scrapeRecipe(1)
                except RuntimeError:
                    if self.logging_level == "DEBUG": logging.debug("Hupala occured")
                    print("Hupala")

        recipe_url = scraper.canonical_url()
        if self.logging_level == "DEBUG": logging.debug(f"got new URL {recipe_url}")
        title = scraper.title()
        image_url = scraper.image()
        char_to_remove = ["-", "\"", "\'"]
        for char in char_to_remove:
            title = title.replace(char, "")
        ingreds = scraper.ingredients()
        
        if not self.table_exists(title):
            try:
                print(f"adding {title}")
                if self.logging_level == "DEBUG": logging.debug(f"adding {title}")
                self.cur.execute("CREATE TABLE '{}' (ingred text, recipe_url text, image_url text)".format(title))
            except:
                print(f"tried to add {title} a table that already existed, table_exists failed")
            for ingred in ingreds:
                if self.logging_level == "DEBUG": logging.debug(f"adding {ingred} to table {title}")
                self.cur.execute(" insert into '{}' values (?, ?, ?)".format(title), (ingred, recipe_url, image_url))
        else:
            print(f"recipe already exists {title}")
        self.con.commit()
