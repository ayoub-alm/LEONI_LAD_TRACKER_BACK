from functools import wraps

from flask import Flask, jsonify, request
import jwt
from database import db
from models.harness import HarnessModel
from services.authentication import Authentication
from services.harness_service import HarnessService
from services.prod_harness_service import ProdHarnessService
from services.production_job_service import ProductionJobService
from services.project import ProjectService
from services.production_line_service import ProductionLineService
from flask_cors import CORS
from models.production_job import ProductionJob

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/leoni_tracker'
app.config.from_object('config')
db.init_app(app)
CORS(app)

# Create database tables
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print("Error creating tables:", e)


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


# Projects routes
@app.route('/projects')
# @token_required(['admin'])
def get_all_project():
    project_service = ProjectService()
    return project_service.get_all_project()


# Production lines routes
@app.route('/production-lines')
# @token_required(['admin'])
def get_all_production_lines():
    production_lines = ProductionLineService.get_all_production_lines()
    production_lines_dicts = [production_line.to_dict() for production_line in production_lines]
    return jsonify(production_lines_dicts), 200


@app.route('/production-lines', methods=['POST'])
def create_production_line():
    data = request.json
    name = data.get('name')
    number_of_operators = data.get('number_of_operators', 0)
    project_id = data.get('project_id')

    production_line = ProductionLineService.create(name, number_of_operators, project_id)
    return jsonify(production_line.to_dict()), 201


@app.route('/production-lines/<int:production_line_id>', methods=['GET'])
def get_production_line(production_line_id):
    production_line = ProductionLineService.get_by_id(production_line_id)
    if production_line:
        return jsonify(production_line.to_dict()), 200
    else:
        return jsonify({'error': 'Production line not found'}), 404


@app.route('/production-lines/<int:production_line_id>', methods=['PUT'])
def update_production_line(production_line_id):
    data = request.json
    name = data.get('name')
    number_of_operators = data.get('number_of_operators')
    project_id = data.get('project_id')

    updated_production_line = ProductionLineService.update(production_line_id, name, number_of_operators, project_id)

    if updated_production_line:
        return jsonify(updated_production_line.to_dict()), 200
    else:
        return jsonify({'error': 'Production line not found'}), 404


@app.route('/production-lines/<int:production_line_id>', methods=['DELETE'])
def delete_production_line(production_line_id):
    success = ProductionLineService.delete(production_line_id)
    if success:
        return jsonify({'message': 'Production line deleted successfully'}), 200
    else:
        return jsonify({'error': 'Production line not found'}), 404


# Harness routes
@app.route('/harness', methods=['POST'])
def create_harness():
    data = request.json  # Assuming the request body contains JSON data
    ref = data.get('ref')
    fase_iso = data.get('fase_iso')
    family = data.get('family')
    range_time = data.get('range_time')
    project_id = data.get('project_id')

    harness = HarnessService.create(ref, fase_iso, family, range_time, project_id)

    if harness:
        # Return a JSON response indicating success
        return jsonify({'message': 'Harness created successfully', 'harness_id': harness.id}), 201
    else:
        # Return a JSON response indicating failure
        return jsonify({'error': 'Failed to create harness'}), 400


@app.route('/harness', methods=['GET'])
def get_all_harness():
    harnesses = HarnessService.get_all()
    if len(harnesses):
        # Return a JSON response with the harness details
        return jsonify([harness.to_dict() for harness in harnesses]), 200
    else:
        # Return a JSON response indicating that the harness was not found
        return jsonify({'error': 'Harness not found'}), 404


@app.route('/harness/project/<int:project_id>', methods=['GET'])
def get_all_harness_by_project_id(project_id):
    harness = HarnessModel()
    harnesses = harness.query.filter_by(project_id=project_id).all()
    if len(harnesses):
        # Return a JSON response with the harness details
        return jsonify([harness.to_dict() for harness in harnesses]), 200
    else:
        # Return a JSON response indicating that the harness was not found
        return jsonify({'error': 'Harness not found'}), 404


@app.route('/harness/family/<string:family>', methods=['GET'])
def get_all_harness_by_family(family):
    harness = HarnessModel()
    harnesses = harness.query.filter_by(family=family).all()
    if len(harnesses):
        # Return a JSON response with the harness details
        return jsonify([harness.to_dict() for harness in harnesses]), 200
    else:
        # Return a JSON response indicating that the harness was not found
        return jsonify({'error': 'Harness not found'}), 404


@app.route('/harness/<int:harness_id>', methods=['GET'])
def get_harness(harness_id):
    harness = HarnessService.get_by_id(harness_id)
    if harness:
        # Return a JSON response with the harness details
        return jsonify(harness.to_dict()), 200
    else:
        # Return a JSON response indicating that the harness was not found
        return jsonify({'error': 'Harness not found'}), 404


@app.route('/harness/<int:harness_id>', methods=['PUT'])
def update_harness(harness_id):
    data = request.json
    ref = data.get('ref')
    fase_iso = data.get('fase_iso')
    family = data.get('family')
    range_time = data.get('range_time')
    project_id = data.get('project_id')

    # Update the harness with the provided data
    updated_harness = HarnessService.update(harness_id, ref, fase_iso, family, range_time, project_id)

    if updated_harness:
        # Return a JSON response with the updated harness details
        return jsonify(updated_harness.to_dict()), 200
    else:
        # Return a JSON response indicating that the harness was not found
        return jsonify({'error': 'Harness not found'}), 404


@app.route('/harness/<int:harness_id>', methods=['DELETE'])
def delete_harness(harness_id):
    # Delete the harness with the specified ID
    success = HarnessService.delete(harness_id)
    if success:
        # Return a JSON response indicating success
        return jsonify({'message': 'Harness deleted successfully'}), 200
    else:
        # Return a JSON response indicating that the harness was not found
        return jsonify({'error': 'Harness not found'}), 404


# Production harness routes
@app.route('/prod-harness/<int:prod_harness_id>', methods=['GET'])
def get_prod_harness(prod_harness_id):
    prod_harness = ProdHarnessService.get_by_id(prod_harness_id)
    if prod_harness:
        return jsonify(prod_harness.to_dict()), 200
    else:
        return jsonify({'error': 'Prod harness not found'}), 404


@app.route('/prod-harness', methods=['POST'])
def create_production_harness():
    data = request.json
    uuid = data.get('uuid')
    box_number = data.get('box_number')
    range_time = data.get('range_time')
    production_job_id = data.get('productionJobId')

    # if uuid is None or box_number is None or production_job_id is None:
    #     return jsonify({'error': 'Missing data in request'}), 400

    production_harness = ProdHarnessService.create(uuid, box_number, range_time, production_job_id)
    if production_harness:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': 'Failed to create production harness'}), 400


@app.route('/prod-harness/<int:prod_harness_id>', methods=['PUT'])
def update_prod_harness(prod_harness_id):
    data = request.json
    uuid = data.get('uuid')
    box_number = data.get('box_number')
    range_time = data.get('range_time')
    harness_id = data.get('harness_id')

    updated_prod_harness = ProdHarnessService.update(prod_harness_id, uuid, box_number, range_time, harness_id)

    if updated_prod_harness:
        return jsonify(updated_prod_harness.to_dict()), 200
    else:
        return jsonify({'error': 'Prod harness not found'}), 404


@app.route('/prod-harness/<int:prod_harness_id>', methods=['DELETE'])
def delete_prod_harness(prod_harness_id):
    success = ProdHarnessService.delete(prod_harness_id)
    if success:
        return jsonify({'message': 'Prod harness deleted successfully'}), 200
    else:
        return jsonify({'error': 'Prod harness not found'}), 404


@app.route('/prod-harness', methods=['GET'])
def get_all_prod_harness():
    prod_harnesses = ProdHarnessService.get_all()
    if prod_harnesses:
        return jsonify([prod_harness.to_dict() for prod_harness in prod_harnesses]), 200
    else:
        return jsonify({'error': 'Prod harness not found'}), 404


# Production job routes
@app.route('/production-jobs/<int:production_job_id>', methods=['GET'])
def get_production_job(production_job_id):
    production_job = ProductionJobService.get_by_id(production_job_id)
    if production_job:
        return jsonify(production_job.to_dict()), 200
    else:
        return jsonify({'error': 'Production job not found'}), 404


@app.route('/production-jobs/line/<int:production_line_id>', methods=['GET'])
def get_current_production_job(production_line_id):
    production_job = ProductionJobService.get_current_production_job_by_line(production_line_id)
    if production_job:
        return jsonify(production_job.to_dict()), 200
    else:
        return jsonify({'error': 'Production job not found'}), 404


@app.route('/production-jobs/line/awaiting/<int:production_line_id>', methods=['GET'])
def get_awaiting_production_job_per_line(production_line_id):
    production_jobs = ProductionJobService.get_awaiting_production_job_by_line(production_line_id)
    if production_jobs:
        return jsonify([production_job.to_dict() for production_job in production_jobs]), 200
    else:
        return jsonify({'error': 'Production job not found'}), 404


@app.route('/production-jobs', methods=['POST'])
def create_production_job():
    print(request.json)
    production_job_data = request.json
    harness_id = production_job_data.get('harness_id')
    quantity = production_job_data.get('quantity')
    production_line_id = production_job_data.get('production_line_id')
    # project_id = production_job_data.get('project_id')
    production_job = ProductionJobService.create(1, harness_id, quantity, 0)
    if production_job:
        return jsonify(production_job.to_dict()), 200
    else:
        return jsonify({'error': 'Production job not found'}), 404


@app.route('/production-jobs', methods=['GET'])
def get_production_jobs():
    production_jobs = ProductionJobService.get_all()
    if len(production_jobs):

        return jsonify([job.to_dict() for job in production_jobs]), 200
    else:
        return jsonify({'error': 'Production job not found'}), 404


@app.route('/production-jobs/<int:production_job_id>', methods=['PUT'])
def update_production_job(production_job_id):
    data = request.json
    uuid = data.get('uuid')
    production_line_id = data.get('production_line_id')
    harness_id = data.get('harness_id')
    demanded_quantity = data.get('demanded_quantity')
    delivered_quantity = data.get('delivered_quantity')

    updated_production_job = ProductionJobService.update(production_job_id, uuid, production_line_id, harness_id,
                                                         demanded_quantity, delivered_quantity)

    if updated_production_job:
        return jsonify(updated_production_job.to_dict()), 200
    else:
        return jsonify({'error': 'Production job not found'}), 404


@app.route('/production-jobs/<int:production_job_id>', methods=['DELETE'])
def delete_production_job(production_job_id):
    success = ProductionJobService.delete(production_job_id)
    if success:
        return jsonify({'message': 'Production job deleted successfully'}), 200
    else:
        return jsonify({'error': 'Production job not found'}), 404


# Authentication routes
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
    app.run(debug=True)
