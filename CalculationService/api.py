from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculation.db'
db = SQLAlchemy(app)

# Модель для бюджету
class BudgetModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_budget = db.Column(db.Float, default=30000.0)  # Початковий бюджет

# Модель для історії витрат
class ExpenseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)  # Ім'я користувача
    expense_amount = db.Column(db.Float, nullable=False)  # Сума витрат

with app.app_context():
    db.create_all()
    # Ініціалізація бюджету, якщо ще не створений
    if not BudgetModel.query.first():
        initial_budget = BudgetModel(total_budget=30000.0)
        db.session.add(initial_budget)
        db.session.commit()

# Ресурс для роботи з бюджетом
class Budget(Resource):
    def get(self):
        budget = BudgetModel.query.first()
        if not budget:
            return {"message": "Budget not found"}, 404

        # Отримуємо історію витрат
        expenses = ExpenseModel.query.all()
        expense_list = [{"user_name": e.user_name, "expense_amount": e.expense_amount} for e in expenses]

        return {"total_budget": budget.total_budget, "expenses": expense_list}, 200

    def patch(self):
        data = request.get_json()
        budget = BudgetModel.query.first()
        if not budget:
            return {"message": "Budget not found"}, 404
        if "expense" in data and "user_name" in data:
            # Віднімаємо витрати від бюджету
            budget.total_budget -= data["expense"]
            # Додаємо запис про витрати
            new_expense = ExpenseModel(user_name=data["user_name"], expense_amount=data["expense"])
            db.session.add(new_expense)
        db.session.commit()
        return {"total_budget": budget.total_budget}, 200

    def post(self):
        # Скидаємо бюджет до початкового значення
        budget = BudgetModel.query.first()
        if not budget:
            return {"message": "Budget not found"}, 404
        budget.total_budget = 30000.0  # Початкове значення

        # Очищуємо історію витрат
        ExpenseModel.query.delete()
        db.session.commit()
        return {"message": "Budget and expenses reset successfully"}, 200

api.add_resource(Budget, "/budget")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
