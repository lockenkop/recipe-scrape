import sqlite3
from chefkoch import recipeScraper

chefkoch = recipeScraper()
con = sqlite3.connect('recipes.db')

cur = con.cursor()
print(chefkoch.table_exists("Mousse au chocolat"))


cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

tables = cur.fetchall()
print(len(tables))
for table in tables:
    if table[0].find("Italienischer Nudelsalat") > -1:
        print(table)