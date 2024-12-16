from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
import requests
from . import UserModel
from . import db

views = Blueprint('views', __name__)
BASE_CALC = "http://127.0.0.1:5002/budget"

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        expense = request.form.get('expense')
        if expense:
            user = UserModel.query.filter_by(id=current_user.id).first()
            if user:
                # Збереження витрат у базу даних
                user.expense = float(expense)
                db.session.commit()

            # Передаємо ім'я користувача разом із витратами до зовнішнього сервісу
            requests.patch(BASE_CALC, json={"expense": float(expense), "user_name": current_user.name})
        return redirect(url_for('views.home'))

    # Отримуємо поточний бюджет та історію витрат із BudgetService
    budget_data = requests.get(BASE_CALC).json()
    total_budget = budget_data.get("total_budget", 0)
    expenses = budget_data.get("expenses", [])
    return render_template("home.html", user=current_user, total_budget=total_budget, expenses=expenses)

@views.route('/reset', methods=['POST'])
@login_required
def reset_budget():
    # Скидаємо бюджет у базі даних
    users = UserModel.query.all()
    for user in users:
        user.expense = 0
    db.session.commit()
    return redirect(url_for('views.home'))
