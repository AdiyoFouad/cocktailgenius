from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import Student
from database import db

student_blueprint = Blueprint('student', __name__)



main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
@main_blueprint.route('/home')
def index():
    return render_template('index.html')

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



































@student_blueprint.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data inserted successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        new_student = Student(name=name, email=email, phone=phone)
        db.session.add(new_student)
        db.session.commit()

        """return jsonify({'message': 'Inscription réussie'}), 201"""

        return redirect(url_for('index'))


@student_blueprint.route('/students')
def get_students():
    students = Student.query.all()
    return students

@student_blueprint.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == "POST":
        id_data = request.form['id_user']
       

        student = db.session.query(Student).filter(Student.id_user == id_data).first()
        student.name = request.form['name']
        student.email = request.form['email']
        student.phone = request.form['phone']

        db.session.commit()

        
        flash("Data updated successfully")
    return redirect(url_for('index'))