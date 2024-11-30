from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import requests

views = Blueprint('views', __name__)
BASE_CALC = "http://192.168.1.123:5002/budget"

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        expense = request.form.get('expense')
        # Передаємо ім'я користувача разом із витратами
        requests.patch(BASE_CALC, json={"expense": float(expense), "user_name": current_user.name})
        return redirect(url_for('views.home'))

    # Отримуємо поточний бюджет та історію витрат із CalculationService
    budget_data = requests.get(BASE_CALC).json()
    total_budget = budget_data.get("total_budget", 0)
    expenses = budget_data.get("expenses", [])
    return render_template("home.html", user=current_user, total_budget=total_budget, expenses=expenses)

@views.route('/reset', methods=['POST'])
@login_required
def reset_budget():
    # Викликаємо API для скидання бюджету
    requests.post(BASE_CALC)
    return redirect(url_for('views.home'))
