from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import User
from database import db



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
            

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('next', None)
    return redirect(url_for('main.index'))





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






