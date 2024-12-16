from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:Nikolas2815@userdb.c54yg0ggumzr.eu-central-1.rds.amazonaws.com:5432/user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель UserModel
class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

with app.app_context():
    db.create_all()

# Аргументы для создания нового пользователя
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("email", type=str, help="User email", required=True)
user_put_args.add_argument("password", type=str, help="User password", required=True)
user_put_args.add_argument("name", type=str, help="User name", required=True)

# Аргументы для обновления пользователя
user_update_args = reqparse.RequestParser()
user_update_args.add_argument("email", type=str, help="User email")
user_update_args.add_argument("password", type=str, help="User password")
user_update_args.add_argument("name", type=str, help="User name")

# Поля для ответа
resource_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password': fields.String,
    'name': fields.String,
}

class UserDB(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id=None):
        email = request.args.get('email')
        if email:
            result = UserModel.query.filter_by(email=email).first()
            if not result:
                abort(404, message="User with this email not found")
            return result

        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()

        # Проверка: существует ли пользователь с данным ID
        existing_user = UserModel.query.filter_by(id=user_id).first()
        if existing_user:
            abort(409, message="User with this ID already exists.")

        # Проверка: существует ли пользователь с данным email
        existing_email = UserModel.query.filter_by(email=args['email']).first()
        if existing_email:
            abort(409, message="User with this email already exists.")

        # Создаем нового пользователя
        user = UserModel(
            id=user_id,
            email=args['email'],
            password=args['password'],
            name=args['name']
        )
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update")
        if args['email']:
            result.email = args['email']
        if args['password']:
            result.password = args['password']
        if args['name']:
            result.name = args['name']
        db.session.commit()
        return result

    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User doesn't exist, cannot delete")
        db.session.delete(user)
        db.session.commit()
        return "User deleted successfully", 200

api.add_resource(UserDB, "/userDB/<int:user_id>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
