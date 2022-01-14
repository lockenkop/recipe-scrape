from flask import Flask, render_template, request
from chefkoch import RecipeScraper




app = Flask(__name__)

chefkoch = RecipeScraper()

@app.route("/")
def index():
    chefkoch = RecipeScraper()
    amount = chefkoch.recipe_amount()
    return render_template('base.html', amount=amount)

@app.route("/", methods = ['POST'])
def ingred_search():
    print("searching")
    
    chefkoch = RecipeScraper()
    amount = chefkoch.recipe_amount()
    ingreds = request.form['ingreds']
    name_to_search = request.form['recipe_name']
    if ingreds:
        ingreds_list = ingreds.split()
        print(ingreds_list)
        found_recipes = chefkoch.search_ingred(ingreds_list)
        return render_template('show_urls.html', urls=found_recipes, ingreds=ingreds, amount=amount)
    if name_to_search:  
        found_recipes = chefkoch.showRecipe(name_to_search)
        return render_template('show_urls.html', urls=found_recipes, name=name_to_search, amount=amount)
    return "NÖ"