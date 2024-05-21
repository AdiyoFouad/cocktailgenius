from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from routes import  cocktail_blueprint, main_blueprint
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fouad:adiyo@localhost/cocktailgenius'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

db.init_app(app)
jwt = JWTManager(app)



app.register_blueprint(main_blueprint)
app.register_blueprint(cocktail_blueprint)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
