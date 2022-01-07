from os import name
import re
import sqlite3

from recipe_scrapers import scrape_me

con = sqlite3.connect('recipes.db')
cur = con.cursor()

URL = "https://www.chefkoch.de/rezepte/zufallsrezept/"

def search_ingred(ingred_to_search):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

    table_names = cur.fetchall()
    # print(table_names)
    querry = ""
    for table_name in table_names:
        for ingred in ingred_to_search:
            querry = querry + "SELECT url FROM '{}' WHERE ingred LIKE '%{}%'".format(table_name[0], ingred)
            querry = querry + " UNION "
    print(querry[:-6])
    
    cur.execute(querry)
    results = cur.fetchall()
    if results:
        print({table_name[0]})
        print(results[0])

def table_exists(db, name):
    query = "SELECT 1 FROM sqlite_master WHERE type='table' and name = ?"
    return db.execute(query, (name,)).fetchone() is not None

def main():
    scraper = scrape_me(URL)
    recipe_url = scraper.canonical_url()
    title = scraper.title().replace("-", "")
    ingreds = scraper.ingredients()
    yields = scraper.yields()

    if not yields:
        yields = 1
    else:
        yields = re.findall(r'\d+', yields)[0]
   

    ingred_list = ["Salz", "Eier"]
    search_ingred(ingred_list)

    con.close()

if __name__ == "__main__":
    main()