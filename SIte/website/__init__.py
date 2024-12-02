from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin
import requests

BASE = "http://192.168.1.123:5001/"

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user_data = requests.get(BASE + "userDB/" + id).json()
        if 'id' in user_data:
            user_id = user_data['id']
        else:
            return None
        if 'email' in user_data:
            user_email = user_data['email']
        if 'password' in user_data:
            user_password = user_data['password']
        if 'name' in user_data:
            user_name = user_data['name']

        # Створюємо користувача без полів age та weight
        user = UserModel(
            id=user_id,
            email=user_email,
            password=user_password,
            name=user_name
        )
        return user

    return app


class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)


