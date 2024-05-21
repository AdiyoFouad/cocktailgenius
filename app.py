from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from routes import student_blueprint, cocktail_blueprint
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fouad:adiyo@localhost/cocktailgenius'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

db.init_app(app)
jwt = JWTManager(app)



app.register_blueprint(student_blueprint)
app.register_blueprint(cocktail_blueprint)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/submit_recipe')
def submit_recipe():
    return render_template('submit_recipe.html', title= "Submit Recipe")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
