from functools import wraps

from flask import Flask, jsonify, request
import jwt
from database import db
from models.harness import HarnessModel
from services.authentication import Authentication
from services.field_service import FieldService
from services.harness_service import HarnessService
from services.packaging_process_service import PackagingProcessService
from services.packaging_step_service import PackagingStepService
from services.post_service import PostService
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
    production_job = ProductionJobService.create(production_line_id, harness_id, quantity, 0)
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


# Routes for FieldService
@app.route('/fields', methods=['POST'])
def create_field():
    data = request.json
    field = FieldService.create_field(data['name'], data['pre_fix'])
    return jsonify(field.to_dict()), 201


@app.route('/fields/<int:field_id>', methods=['GET'])
def get_field(field_id):
    field = FieldService.get_field_by_id(field_id)
    if field:
        return jsonify(field.to_dict()), 200
    else:
        return jsonify({'error': 'Field not found'}), 404


@app.route('/fields/<int:field_id>', methods=['PUT'])
def update_field(field_id):
    data = request.json
    field = FieldService.update_field(field_id, data.get('name'), data.get('pre_fix'))
    if field:
        return jsonify(field.to_dict()), 200
    else:
        return jsonify({'error': 'Field not found'}), 404


@app.route('/fields/<int:field_id>', methods=['DELETE'])
def delete_field(field_id):
    field = FieldService.delete_field(field_id)
    if field:
        return jsonify(field.to_dict()), 200
    else:
        return jsonify({'error': 'Field not found'}), 404


@app.route('/fields', methods=['GET'])
def get_all_fields():
    fields = FieldService.get_all_fields()
    return jsonify([field.to_dict() for field in fields]), 200


# Routes for PackagingStepService
@app.route('/steps', methods=['POST'])
def create_packaging_step():
    data = request.json
    step = PackagingStepService.create_packaging_step(data['field'], data['status'], data['description'],
                                                      data['packaging_process_step_id'], data['order'])
    return jsonify(step.to_dict()), 201


@app.route('/steps/<int:step_id>', methods=['GET'])
def get_packaging_step(step_id):
    step = PackagingStepService.get_step_by_id(step_id)
    if step:
        return jsonify(step.to_dict()), 200
    else:
        return jsonify({'error': 'Step not found'}), 404


@app.route('/steps/<int:step_id>', methods=['PUT'])
def update_packaging_step(step_id):
    data = request.json
    step = PackagingStepService.update_packaging_step(step_id, data.get('field'), data.get('status'),
                                                      data.get('description'), data.get('order'))
    if step:
        return jsonify(step.to_dict()), 200
    else:
        return jsonify({'error': 'Step not found'}), 404


@app.route('/steps/<int:step_id>', methods=['DELETE'])
def delete_packaging_step(step_id):
    step = PackagingStepService.delete_packaging_step(step_id)
    if step:
        return jsonify(step.to_dict()), 200
    else:
        return jsonify({'error': 'Step not found'}), 404


@app.route('/steps', methods=['GET'])
def get_all_steps():
    steps = PackagingStepService.get_all_steps()
    return jsonify([step.to_dict() for step in steps]), 200


# Routes for PostService
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    post = PostService.create_post(data['name'])
    return jsonify(post.to_dict()), 201


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = PostService.get_post_by_id(post_id)
    if post:
        return jsonify(post.to_dict()), 200
    else:
        return jsonify({'error': 'Post not found'}), 404


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    post = PostService.update_post(post_id, data.get('name'))
    if post:
        return jsonify(post.to_dict()), 200
    else:
        return jsonify({'error': 'Post not found'}), 404


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = PostService.delete_post(post_id)
    if post:
        return jsonify(post.to_dict()), 200
    else:
        return jsonify({'error': 'Post not found'}), 404


@app.route('/posts', methods=['GET'])
def get_all_posts():
    posts = PostService.get_all_posts()
    return jsonify([post.to_dict() for post in posts]), 200


# Create a new packaging process
@app.route('/processes', methods=['POST'])
def create_process():
    data = request.json
    process = PackagingProcessService.create_process(data['family_id'], data['status'], data['name'])
    return jsonify(process.to_dict()), 201


# Retrieve a packaging process by ID
@app.route('/processes/<int:process_id>', methods=['GET'])
def get_process(process_id):
    process = PackagingProcessService.get_process_by_id(process_id)
    if process:
        return jsonify(process.to_dict()), 200
    else:
        return jsonify({'error': 'Process not found'}), 404


# Update a packaging process by ID
@app.route('/processes/<int:process_id>', methods=['PUT'])
def update_process(process_id):
    data = request.json
    process = PackagingProcessService.update_process(process_id, data.get('family_id'), data.get('status'),
                                                     data.get('name'))
    if process:
        return jsonify(process.to_dict()), 200
    else:
        return jsonify({'error': 'Process not found'}), 404


# Delete a packaging process by ID
@app.route('/processes/<int:process_id>', methods=['DELETE'])
def delete_process(process_id):
    process = PackagingProcessService.delete_process(process_id)
    if process:
        return jsonify(process.to_dict()), 200
    else:
        return jsonify({'error': 'Process not found'}), 404


# Retrieve all packaging processes
@app.route('/processes', methods=['GET'])
def get_all_processes():
    processes = PackagingProcessService.get_all_processes()
    return jsonify([process.to_dict() for process in processes]), 200


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


if __name__ == "__main__":
    app.run()
