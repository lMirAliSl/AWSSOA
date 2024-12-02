from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests
from . import UserModel

auth = Blueprint('auth', __name__)
BASE = "http://127.0.0.1:5001/userDB"

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Виконуємо GET-запит, щоб знайти користувача за email
        response = requests.get(BASE + "/0", params={"email": email})
        if response.status_code == 200:
            user_data = response.json()
            if 'password' in user_data and check_password_hash(user_data['password'], password):
                flash('Logged in successfully!', category='success')
                user = UserModel(
                    id=user_data['id'],
                    email=user_data['email'],
                    password=user_data['password'],
                    name=user_data['name']
                )
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Перевірки полів
        if password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Відправка даних нового користувача в API
            new_user = {
                "email": email,
                "password": generate_password_hash(password1, method='pbkdf2:sha256'),
                "name": name
            }
            response = requests.put(BASE + "/0", json=new_user)
            if response.status_code == 201:
                flash('Account created successfully!', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('An error occurred during registration.', category='error')

    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
