from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from routes import  cocktail_blueprint, main_blueprint, user_blueprint
from database import db
from models import User
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql://fouad:adiyo@localhost/cocktailgenius')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','your_secret_key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY','jwt_secret_key')

db.init_app(app)
jwt = JWTManager(app)



app.register_blueprint(main_blueprint)
app.register_blueprint(cocktail_blueprint)
app.register_blueprint(user_blueprint)

# Configuration of Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
