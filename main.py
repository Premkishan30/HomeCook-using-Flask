import glob
import this
from hashlib import new
from urllib.parse import urlencode


class data():
    searchedFile = ""


from flask import Flask, render_template, request, redirect, flash, send_file
import os

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Python MP'

f = data()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/nav")
def nav():
    return render_template('navbar.html')


@app.route('/submit_recipe', methods=['POST'])
def submit_recipe():
    name = request.form['name']
    email1 = request.form.get('email')
    recipe_name = request.form['recipe-name']
    ingredients = request.form['ingredients']
    step1 = request.form['step1']
    step2 = request.form['step2']
    step3 = request.form['step3']
    step4 = request.form['step4']
    filename = 'Recipes/' + recipe_name + '.txt'

    recipes_new = {
        "Name": name,
        "Email": email1,
        "Recipe Name": recipe_name,
        "Ingredients": ingredients,
        "Step 1": step1,
        "Step 2": step2,
        "Step 3": step3,
        "Step 4": step4
    }

    with open(filename, 'w') as file:
        for key, value in recipes_new.items():
            file.write(f"{key}:{value}\n")
    flash("Recipe Submitted Sucessfully", "success")
    return render_template('home.html')


@app.route("/search")
def search():
    return render_template('search.html')


@app.route("/result", methods=['POST'])
def result():
    recipe_name1 = request.form.get('recipe-name')
    filename = recipe_name1 + '.txt'
    folder = 'Recipes'
    dir1 = os.path.join(os.getcwd(), folder)
    match_file = glob.glob(os.path.join(dir1, f"*{filename}"))
    print(os.listdir(dir1))
    if len(match_file) > 0:
        f.searchedFile = match_file[0]
        print(f.searchedFile)
        return redirect('/recipe')
    else:
        flash("FILE NOT FOUND!!!", 'error')
        f.searchedFile = ""
        return render_template('search.html')


@app.route('/recipe')
def recipe():
    print(f.searchedFile)
    if len(f.searchedFile) == 0:
        return "<h1>No Recipe is Searched</h1>"
    else:

        with open(f.searchedFile, 'r') as file:
            data1 = file.read()
            data_d = {}

            for line in data1.split('\n'):
                if line:
                    key, value = line.split(':')
                    data_d[key.strip()] = value.strip()
        return render_template('Recipe.html', data_d=data_d)


@app.route('/download')
def download():
    return send_file(f.searchedFile, as_attachment=True)


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)
