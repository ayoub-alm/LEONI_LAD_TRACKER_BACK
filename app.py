from functools import wraps

from flask import Flask, jsonify, request
import jwt
from database import db
from services.authentication import Authentication
from services.project import ProjectService
from services.production_line import ProductionLineService
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/leoni_tracker'
# app.config.from_object('config')
db.init_app(app)
CORS(app)

# Create database tables
with app.app_context():
    db.create_all()


def token_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            print(*args)
            token = request.args.get('token')

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                if data.get('user').get('role') not in roles:
                    return jsonify({'message': 'Unauthorized access'}), 403
            except:
                return jsonify({'message': 'Token is invalid!'}), 401

            return f(*args, **kwargs)

        return decorated
    return decorator


@app.route('/projects')
@token_required(['admin'])
def get_all_project():
    project_service = ProjectService()
    return project_service.get_all_project()


@app.route('/production-lines')
@token_required(['admin'])
def get_all_production_lines():
    return ProductionLineService.get_all_production_lines()


@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    email = auth.get('email')
    password = auth.get('password')

    if email is None or password is None:
        return jsonify({'error': 'Missing email or password'}), 400

    auth_service = Authentication()
    return auth_service.login(email, password)


if __name__ == '__main__':
    app.run()
