from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import User, Recipe, Ingredient, RecipeIngredient, Step, Rating, Comment
from database import db
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/images/users_avatar'
UPLOAD_RECIPE_FOLDER = 'static/images/recipes_images'


main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
@main_blueprint.route('/home')
def index():
    return render_template('index.html')

@main_blueprint.route('/login')
def login():
    session['next'] = request.args.get('next')
    return render_template('login.html')

@main_blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@main_blueprint.route('/profil', methods = ['POST', 'GET'])
@login_required
def profil():
    return render_template('profil.html', title= "Profile")

@main_blueprint.route('/submit_recipe')
@login_required
def submit_recipe():
    return render_template('submit_recipe.html', title= "Submit Recipe")


user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/new_user', methods = ['POST'])
def new_user():
    if (request.method == 'POST'):
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        n_user  = User(username=username, firstname=first_name, lastname=last_name, email = email, password=password)
 
        db.session.add(n_user)
        db.session.commit()
        flash("Your account has been successfully created")
        return render_template(url_for('/user_login'), title = "Login")


@user_blueprint.route('/user_login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False         
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user, remember=remember)
            if session.get('next'):
                next_url = session.get('next')
                session.pop('next')
                return redirect(next_url or url_for('main.index'))
            else:
                return render_template('cocktails.html', title="Cocktails")
        else:
            flash('Invalid username or password', 'error')
            if session.get('next'):
                next_url = session.get('next')
                return redirect(url_for('user.user_login', next=next_url))
            else:
                return redirect(url_for('user.user_login'))
    else:
        return render_template('login.html')


@user_blueprint.route('/update_profil_image', methods=['POST', 'GET'])
@login_required
def update_profil_image():
    if request.method == 'POST':
        file = request.files['avatar']
        file_extension = os.path.splitext(file.filename)[1]
        filename = 'avatar_{}{}'.format(current_user.id, file_extension)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        current_user.profile_image = os.path.join('images/users_avatar', filename).replace('\\', '/')
        db.session.commit()
        
        flash('Profile image updated successfully.', 'success')
        return redirect(url_for('main.profil'))

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('next', None)
    return redirect(url_for('main.index'))





cocktail_blueprint = Blueprint('cocktail', __name__)

@cocktail_blueprint.route('/cocktails')
def cocktails():
    cocktails = Recipe.query.all()
    return render_template('cocktails.html', title="Cocktails", cocktails = cocktails)

@cocktail_blueprint.route('/cocktail/<int:cocktail_id>')
def details_cocktail(cocktail_id):
    cocktail = Recipe.query.filter_by(id=cocktail_id).first()
    return render_template('details.html', title="Cocktail Details", cocktail = cocktail)

@cocktail_blueprint.route('/new_cocktail', methods=['POST'])
def new_cocktail():
    if request.method == "POST":
        title = request.form['nom']
        difficulty = request.form['difficulte']
        ingredients_concatenated = request.form['ingredientsConcatenated']
        steps_concatenated = request.form['etapesConcatenated']
        image_file = request.files['image']

        
        new_recipe = Recipe(title=title, difficulty=difficulty, user_id=current_user.id)

        
        ingredients = ingredients_concatenated.split('\n')
        
        for ingredient in ingredients:
            if ':' not in ingredient:
                continue
            ingredient_name, quantity = ingredient.split(':')
            ingredient_obj = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient_obj:
                ingredient_obj = Ingredient(name=ingredient_name)
                db.session.add(ingredient_obj)
                db.session.commit()
            recipe_ingredient = RecipeIngredient(quantity=quantity, ingredient_id=ingredient_obj.id)
            new_recipe.recipe_ingredients.append(recipe_ingredient)

        
        steps = steps_concatenated.split('\n')
        for step_description in steps:
            if step_description.strip():
                step = Step(description=step_description)
                new_recipe.steps.append(step)

        
        if image_file:
            file_extension = os.path.splitext(image_file.filename)[1]
            filename = secure_filename(f"recipe_{title.replace(' ', '_')}{os.path.splitext(image_file.filename)[1]}")
            image_file.save(os.path.join(UPLOAD_RECIPE_FOLDER, filename))
            new_recipe.recipe_image = os.path.join('images/recipes', filename).replace('\\', '/')

        
        db.session.add(new_recipe)
        db.session.commit()

        flash("Submission of new cocktail recipe successfully completed")

        return jsonify({"message": "Successfully Created Cocktail Recipe"}), 201

@cocktail_blueprint.route('/rate_recipe', methods=['POST'])
@login_required
def rate_recipe():
    recipe_id = request.form['recipe']
    existing_rating = Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    
    if existing_rating:
        return jsonify({'message': 'Vous avez déjà noté cette recette.'}), 400
    else:
        rating_score = request.form['rating']
        
        new_rating = Rating(score=rating_score, user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(new_rating)
        db.session.commit()
        
        return jsonify({'message': 'Votre notation a été enregistrée avec succès.'}), 201

@cocktail_blueprint.route('/comment_recipe', methods=['POST'])
@login_required
def comment_recipe():
    return jsonify(request.form)