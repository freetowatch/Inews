from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

class SpoonacularAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.spoonacular.com/recipes"

    def search_recipes(self, query, number=40):
        endpoint = f"{self.base_url}/search"
        params = {
            "apiKey": self.api_key,
            "query": query,
            "number": number
        }

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            return response.json()["results"]
        else:
            return None

    def get_recipe_details(self, recipe_id):
        endpoint = f"{self.base_url}/{recipe_id}/information"
        params = {
            "apiKey": self.api_key,
            "includeNutrition": True  # Include nutrition information
        }

        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return None

# Replace 'YOUR_SPOONACULAR_API_KEY' with your actual Spoonacular API key
spoonacular_api = SpoonacularAPI(api_key='31f53b3ca4f943449727a5b09e2732d8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    recipes = spoonacular_api.search_recipes(query)

    if recipes:
        return render_template('result.html', recipes=recipes)
    else:
        return render_template('result.html', error="No recipes found.")

@app.route('/recipe/<recipe_id>')
def recipe_details(recipe_id):
    recipe_details = spoonacular_api.get_recipe_details(recipe_id)

    if recipe_details:
        return render_template('recipe_details.html', recipe_details=recipe_details)
    else:
        return render_template('recipe_details.html', error="Recipe details not found.")

if __name__ == '__main__':
    app.run(debug=True)