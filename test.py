import sqlite3

con = sqlite3.connect('recipes.db')
cur = con.cursor()
title  = "Tarte au Chocolat"

char_to_remove = ["-", "\"", "\'"]
for char in char_to_remove:
    title = title.replace(char, "")
print(title)