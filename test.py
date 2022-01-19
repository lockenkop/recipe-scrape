import sqlite3

from chefkoch import RecipeScraper

chefkoch = RecipeScraper()

con = sqlite3.connect('recipes.db')
cur = con.cursor()


chefkoch.scrapeRecipe("inf")

# text = "Salz Pfeffer"
# text_list = list(text)
# print(text_list)

# ingreds= ["Salz", "Pfeffer"]
# result = chefkoch.search_ingred(ingreds)
# print(result)

# title  = "Tarte au Chocolat"
# char_to_remove = ["-", "\"", "\'"]
# for char in char_to_remove:
#     title = title.replace(char, "")
# print(title)