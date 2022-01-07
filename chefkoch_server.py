import recipe_scrapers
import flask
from chefkoch import recipeScraper

chefkoch = recipeScraper()

# print(chefkoch.table_exists('Saftiger Marmorkuchen'))
# chefkoch.search_ingred(["Salz", "Pfeffer", "Muskat", "Ei", "Butter", "Kartoffel", "Speck", "Trauben"])
chefkoch.scrapeRecipe("inf")
