from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import User
from database import db

student_blueprint = Blueprint('student', __name__)



main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
@main_blueprint.route('/home')
def index():
    return render_template('index.html')

@main_blueprint.route('/login')
def login():
    return render_template('login.html')

@main_blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@main_blueprint.route('/profil')
def profil():
    return render_template('profil.html')

@main_blueprint.route('/submit_recipe')
def submit_recipe():
    return render_template('submit_recipe.html', title= "Submit Recipe")




cocktail_blueprint = Blueprint('cocktail', __name__)

@cocktail_blueprint.route('/cocktails')
def cocktails():
    return render_template('cocktails.html', title="Cocktails")

@cocktail_blueprint.route('/cocktail/<int:cocktail_id>')
def details_cocktail(cocktail_id):
    return render_template('details.html', title="Cocktail Details", cocktail = cocktail_id)

@cocktail_blueprint.route('/new_cocktail', methods=['POST'])
def new_cocktail():
    if request.method == "POST":
        flash("Soumission de la nouvelle recette de cocktail effectué avec succès")

        return jsonify(request.form), 201

        """return redirect(url_for('index'))"""











