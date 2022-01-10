from flask import Flask, render_template, request
from chefkoch import RecipeScraper


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('base.html')

@app.route("/", methods = ['POST'])
def ingred_search():
    chefkoch = RecipeScraper()
    ingreds = request.form['ingreds']
    name_to_search = request.form['recipe_name']
    if ingreds:
        ingreds_list = ingreds.split()
        print(ingreds_list)
        found_recipes = chefkoch.search_ingred(ingreds_list)
        return render_template('show_urls.html', urls=found_recipes, ingreds=ingreds)
    if name_to_search:  
        found_recipes = chefkoch.showRecipe(name_to_search)
        return render_template('show_urls.html', urls=found_recipes, name=name_to_search)
    return name_to_search