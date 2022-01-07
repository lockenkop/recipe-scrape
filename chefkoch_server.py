from flask import Flask, render_template, request
from chefkoch import RecipeScraper



# print(chefkoch.table_exists('Saftiger Marmorkuchen'))
# chefkoch.search_ingred(["Salz", "Pfeffer", "Muskat", "Ei", "Butter", "Kartoffel", "Speck"])
# chefkoch.scrapeRecipe("inf")


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods = ['POST'])
def ingred_search():
    chefkoch = RecipeScraper()
    ingreds = request.form['ingreds']
    ingreds_list = ingreds.split()
    print(ingreds_list)
    found_recipes = chefkoch.search_ingred(ingreds_list)
    return render_template('show_urls.html', urls=found_recipes, ingreds=ingreds)