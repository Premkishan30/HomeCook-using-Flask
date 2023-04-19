import glob
import this
from hashlib import new
from urllib.parse import urlencode

from werkzeug.utils import secure_filename


class data():
    searchedFile = ""
    ImageFileName = ["Chicken_Biryani.jpg","Manchurian.jpg"]


from flask import Flask, render_template, request, redirect, flash, send_file
import os

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static')

app.secret_key = 'Python MP'

f = data()


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
    filename1 = 'Recipes/' + recipe_name + '.txt'

    image = request.files['image']

    if image.filename != '':
        filename = secure_filename(recipe_name) + '.' + image.filename.rsplit('.', 1)[1]
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'Imgs', filename))
        f.ImageFileName.append(filename)
        f.ImageFileName.append("")
    else:
        filename = None

    recipes_new = {
        "Name": name,
        "Email": email1,
        "Recipe Name": recipe_name,
        "Ingredients": ingredients,
        "Step 1": step1,
        "Step 2": step2,
        "Step 3": step3,
        "Step 4": step4,
        "Image": filename
    }

    with open(filename1, 'w') as file:
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


@app.route('/')
def displayHome():
    Images = f.ImageFileName
    folder = 'Recipes'
    dir1 = os.path.join(os.getcwd(), folder)
    recipeName = os.listdir(dir1)
    print(Images)
    print(os.listdir(dir1))

    return render_template('Display.html', imgs=Images, names=recipeName)


@app.route('/editrecipe/<recipe>', methods=['GET', 'POST'])
def editRecipe(recipe):
    folder = 'Recipes'
    dir1 = os.path.join(os.getcwd(), folder)
    file_path = os.path.join(dir1, recipe + '.txt')
    with open(file_path, 'r') as file:
        lines = file.readlines()
        ingredients = ''
        step1 = ''
        step2 = ''
        step3 = ''
        step4 = ''
        for line in lines:
            if line.startswith('Ingredients:'):
                ingredients = line.split(' ', 1)[1].strip()
            elif line.startswith('Step 1:'):
                step1 = line.split(' ', 1)[1].strip()
            elif line.startswith('Step 2:'):
                step2 = line.split(' ', 1)[1].strip()
            elif line.startswith('Step 3:'):
                step3 = line.split(' ', 1)[1].strip()
            elif line.startswith('Step 4:'):
                step4 = line.split(' ', 1)[1].strip()

    if request.method == 'POST':
        newIngredients = request.form.get('newIng')
        newStep1 = request.form.get('newStep1')
        newStep2 = request.form.get('newStep2')
        newStep3 = request.form.get('newStep3')
        newStep4 = request.form.get('newStep4')
        with open(file, 'r') as file:
            lines = file.readlines()

        with open(file, 'w') as file:
            for line in lines:
                if line.startswith('Ingredients:'):
                    file.write('Ingredients: ' + newIngredients + '\n')
                elif line.startswith('Step 1:'):
                    file.write('Step 1: ' + newStep1 + '\n')
                elif line.startswith('Step 2:'):
                    file.write('Step 2: ' + newStep2 + '\n')
                elif line.startswith('Step 3:'):
                    file.write('Step 3: ' + newStep3 + '\n')
                elif line.startswith('Step 4:'):
                    file.write('Step 4: ' + newStep4 + '\n')
                else:
                    file.write(line)


@app.route('/viewrecipe/<recipe>')
def viewRecipe(recipe):
    folder = 'Recipes'
    dir1 = os.path.join(os.getcwd(), folder,recipe)
    with open(dir1, 'r') as file:
        data1 = file.read()
        data_d = {}

        for line in data1.split('\n'):
            if line:
                key, value = line.split(':')
                data_d[key.strip()] = value.strip()
    return render_template('Recipe.html', data_d=data_d)


if __name__ == '__main__':
    app.run(debug=True)
