import os
from functools import wraps

from flask import Flask, jsonify, request
import jwt
from database import db
from models.harness import HarnessModel
from router.global_dashboard import global_dashboard_bp
from router.line_dashboard import line_dashboard_bp
from services.authentication import Authentication
from services.field_service import FieldService
from services.group_service import GroupService
from services.harness_service import HarnessService
from services.package_service import PackagingTypeService
from services.packaging_box_service import PackagingBoxService
from services.packaging_process_service import PackagingProcessService
from services.packaging_step_service import PackagingStepService
from services.post_service import PostService
from services.prod_harness_service import ProdHarnessService
from services.production_job_service import ProductionJobService
from services.project import ProjectService
from services.production_line_service import ProductionLineService
from flask_cors import CORS
from models.production_job import ProductionJob
from services.segment_service import SegmentService
from services.user_service import UserService

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/leoni_tracker'
app.config.from_object('config')
db.init_app(app)
CORS(app)
db.configure_mappers()
# Create database tables
with app.app_context():
    db.create_all()

# Register the blueprint
app.register_blueprint(line_dashboard_bp)
# Register the global dashboard Lines
app.register_blueprint(global_dashboard_bp)


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


# Harness routes  ****************************

@app.route('/harness', methods=['POST'])
def create_harness():
    data = request.json
    ref = data.get('ref')
    cpn = data.get('cpn')
    fuse_box = data.get('fuse_box')
    range_time = data.get('range_time')
    package_type_id = data.get('package_type_id')
    segment_id = data.get('segment_id')

    try:
        harness = HarnessService.create(ref, cpn, fuse_box, range_time, package_type_id, segment_id)
        return jsonify({'message': 'Harness created successfully', 'harness_id': harness.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/harness', methods=['GET'])
def get_all_harness():
    harnesses = HarnessService.get_all()
    return jsonify([harness.to_dict() for harness in harnesses]), 200


@app.route('/harness/family', methods=['GET'])
def get_all_family_harness():
    families = HarnessService.get_families()
    formatted_results = [{'family': family, 'count': count} for family, count in families]
    return jsonify(formatted_results), 200


@app.route('/harness/project/<int:project_id>', methods=['GET'])
def get_all_harness_by_project_id(project_id):
    harnesses = HarnessModel.query.filter_by(project_id=project_id).all()
    return jsonify([harness.to_dict() for harness in harnesses]), 200


@app.route('/harness/family/<string:family>', methods=['GET'])
def get_all_harness_by_family(family):
    harnesses = HarnessModel.query.filter_by(family=family).all()
    return jsonify([harness.to_dict() for harness in harnesses]), 200


@app.route('/harness/<int:harness_id>', methods=['GET'])
def get_harness(harness_id):
    harness = HarnessService.get_by_id(harness_id)
    if harness:
        return jsonify(harness.to_dict()), 200
    else:
        return jsonify({'error': 'Harness not found'}), 404


@app.route('/harness/ref/<string:harness_ref>', methods=['GET'])
def get_harness_by_ref(harness_ref):
    harnesses = HarnessService.get_by_ref(harness_ref)
    return jsonify([harness.to_dict() for harness in harnesses]), 200


@app.route('/harness/<int:harness_id>', methods=['PUT'])
def update_harness(harness_id):
    data = request.json
    ref = data.get('ref')
    cpn = data.get('cpn')
    fuse_box = data.get('fuse_box')
    range_time = data.get('range_time')
    package_type_id = data.get('package_type_id')
    segment_id = data.get('segment_id')

    try:
        updated_harness = HarnessService.update(harness_id, ref, cpn, fuse_box, range_time, package_type_id, segment_id)
        if updated_harness:
            return jsonify(updated_harness.to_dict()), 200
        else:
            return jsonify({'error': 'Harness not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/harness/<int:harness_id>', methods=['DELETE'])
def delete_harness(harness_id):
    try:
        success = HarnessService.delete(harness_id)
        if success:
            return jsonify({'message': 'Harness deleted successfully'}), 200
        else:
            return jsonify({'error': 'Harness not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


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
    production_job_id = data.get('production_job_id')
    status = data.get('status', 0)
    packaging_box_id = data.get('packaging_box_id')

    production_harness = ProdHarnessService.create(uuid, box_number, range_time, production_job_id, status,
                                                   packaging_box_id)
    if production_harness:
        return jsonify({"response": True}), 201
    else:
        return jsonify({"response": False}), 400


@app.route('/prod-harness/<int:prod_harness_id>', methods=['PUT'])
def update_prod_harness(prod_harness_id):
    data = request.json
    uuid = data.get('uuid')
    box_number = data.get('box_number')
    range_time = data.get('range_time')
    production_job_id = data.get('production_job_id')
    status = data.get('status')
    packaging_box_id = data.get('packaging_box_id')

    updated_prod_harness = ProdHarnessService.update(prod_harness_id, uuid, box_number, range_time, production_job_id,
                                                     status, packaging_box_id)

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
    return jsonify([prod_harness.to_dict() for prod_harness in prod_harnesses]), 200


@app.route('/prod-harness/uuid/<string:uuid>', methods=['GET'])
def get_prod_harness_by_ref(uuid):
    prod_harness = ProdHarnessService.get_by_uuid(uuid)
    if prod_harness:
        return jsonify(prod_harness.to_dict()), 200
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


@app.route('/steps', methods=['POST'])
def create_packaging_step():
    data = request.json
    step = PackagingStepService.create_packaging_step(
        pre_fix=data['pre_fix'],
        field=data['field_id'],
        status=data['status'],
        description=data['description'],
        packaging_process_id=data['packaging_process_id'],
        img=data['img'],
        order=data['order']
    )
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
    step = PackagingStepService.update_packaging_step(
        step_id,
        pre_fix=data.get('pre_fix'),
        field=data.get('field_id'),
        status=data.get('status'),
        description=data.get('description'),
        packaging_process_id=data.get('packaging_process_id'),
        img=data.get('img'),
        order=data.get('order')
    )
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


@app.route('/steps/bulk', methods=['POST'])
def create_bulk_packaging_steps():
    data = request.json
    steps = PackagingStepService.create_bulk_packaging_steps(data)
    return jsonify([step.to_dict() for step in steps]), 201


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
@app.route('/packaging-process', methods=['POST'])
def create_process():
    data = request.json
    process = PackagingProcessService.create_process(data['segmentId'], data['status'], data['name'])
    return jsonify(process.to_dict()), 201


# Retrieve a packaging process by ID
@app.route('/packaging-process/<int:process_id>', methods=['GET'])
def get_process(process_id):
    process = PackagingProcessService.get_process_by_id(process_id)
    if process:
        return jsonify(process.to_dict()), 200
    else:
        return jsonify({'error': 'Process not found'}), 404


# Update a packaging process by ID
@app.route('/packaging-process/<int:process_id>', methods=['PUT'])
def update_process(process_id):
    data = request.json
    process = PackagingProcessService.update_process(process_id, data.get('family_id'), data.get('status'),
                                                     data.get('name'))
    if process:
        return jsonify(process.to_dict()), 200
    else:
        return jsonify({'error': 'Process not found'}), 404


# Delete a packaging process by ID
@app.route('/packaging-process/<int:process_id>', methods=['DELETE'])
def delete_process(process_id):
    process = PackagingProcessService.delete_process(process_id)
    if process:
        return jsonify(process.to_dict()), 200
    else:
        return jsonify({'error': 'Process not found'}), 404


#   packaging Box
@app.route('/packaging-process', methods=['GET'])
def get_all_processes():
    processes = PackagingProcessService.get_all_processes()
    return jsonify([process.to_dict() for process in processes]), 200


@app.route('/packaging-process/segment/<int:segment_id>', methods=['GET'])
def get_processes_by_segment_id(segment_id):
    process = PackagingProcessService.get_process_by_segment_id(segment_id)
    return jsonify(process.to_dict()), 200


# packaging box routes
@app.route('/packaging_boxes', methods=['GET'])
def get_packaging_boxes():
    packaging_boxes = PackagingBoxService.get_all_packaging_boxes()
    return jsonify([box.to_dict() for box in packaging_boxes])


@app.route('/packaging_box/<int:box_id>', methods=['GET'])
def get_packaging_box(box_id):
    packaging_box = PackagingBoxService.get_packaging_box_by_id(box_id)
    if packaging_box:
        return jsonify(packaging_box.to_dict())
    return jsonify({'message': 'Packaging box not found'}), 404


@app.route('/packaging_box', methods=['POST'])
def create_packaging_box():
    try:
        data = request.json

        required_fields = ['line_id', 'to_be_delivered_quantity', 'delivered_quantity', 'harness_id', 'status',
                           'created_by', 'barcode']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        packaging_box = PackagingBoxService.create_packaging_box(
            line_id=data['line_id'],
            to_be_delivered_quantity=data['to_be_delivered_quantity'],
            delivered_quantity=data['delivered_quantity'],
            harness_id=data['harness_id'],
            status=data['status'],
            created_by=data['created_by'],
            barcode=data['barcode']
        )
        return jsonify(packaging_box.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/packaging_box/<int:box_id>', methods=['PUT'])
def update_packaging_box(box_id):
    data = request.json
    packaging_box = PackagingBoxService.update_packaging_box(box_id, **data)
    if packaging_box:
        return jsonify(packaging_box.to_dict())
    return jsonify({'message': 'Packaging box not found'}), 404


@app.route('/packaging_box/<int:box_id>', methods=['DELETE'])
def delete_packaging_box(box_id):
    packaging_box = PackagingBoxService.get_packaging_box_by_id(box_id)

    if packaging_box:
        # Pre-fetch the packaging box data as a dictionary before deletion
        packaging_box_data = packaging_box.to_dict()

        # Call the service to delete the packaging box
        PackagingBoxService.delete_packaging_box(box_id)

        # Return the pre-fetched data
        return jsonify(packaging_box_data), 200

    return jsonify({'message': 'Packaging box not found'}), 404


@app.route('/packaging_box/opening-package/<int:line_id>')
def opening_package(line_id):
    packaging_box = PackagingBoxService.get_opened_package(line_id)
    if packaging_box:
        return jsonify(packaging_box.to_dict())
    return jsonify({'message': 'Packaging box not found'}), 404


# Authentication routes
@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    matriculate = auth.get('matriculate')
    password = auth.get('password')

    if matriculate is None or password is None:
        return jsonify({'error': 'Missing email or password'}), 400

    auth_service = Authentication()
    return auth_service.login(matriculate, password)


# *************  user route
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data or not 'role' in data or not 'matriculate' in data:
        return jsonify({'message': 'Invalid input'}), 400
    user = UserService.create_user(data['username'], data['password'], data['role'], data['matriculate'])
    return jsonify(user.to_dict()), 201


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


@app.route('/users', methods=['GET'])
def get_all_users():
    users = UserService.get_all_users()
    return jsonify([user.to_dict() for user in users])


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid input'}), 400
    user = UserService.update_user(user_id, data.get('username'), data.get('password'), data.get('role'),
                                   data.get('matriculate'))
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserService.delete_user(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


# package type ************************

@app.route('/packaging_types', methods=['POST'])
def create_packaging_type():
    data = request.json
    type = data.get('type')
    size = data.get('size')
    weight = data.get('weight')
    new_packaging_type = PackagingTypeService.create_packaging_type(type, size, weight)
    return jsonify(new_packaging_type.to_dict()), 201


@app.route('/packaging_types/<int:packaging_type_id>', methods=['GET'])
def get_packaging_type(packaging_type_id):
    packaging_type = PackagingTypeService.get_packaging_type_by_id(packaging_type_id)
    if packaging_type:
        return jsonify(packaging_type.to_dict())
    return jsonify({'message': 'Packaging Type not found'}), 404


@app.route('/packaging_types', methods=['GET'])
def get_all_packaging_types():
    packaging_types = PackagingTypeService.get_all_packaging_types()
    return jsonify([pt.to_dict() for pt in packaging_types])


@app.route('/packaging_types/<int:packaging_type_id>', methods=['PUT'])
def update_packaging_type(packaging_type_id):
    data = request.json
    type = data.get('type')
    size = data.get('size')
    weight = data.get('weight')
    updated_packaging_type = PackagingTypeService.update_packaging_type(packaging_type_id, type, size, weight)
    if updated_packaging_type:
        return jsonify(updated_packaging_type.to_dict())
    return jsonify({'message': 'Packaging Type not found'}), 404


@app.route('/packaging_types/<int:packaging_type_id>', methods=['DELETE'])
def delete_packaging_type(packaging_type_id):
    deleted_packaging_type = PackagingTypeService.delete_packaging_type(packaging_type_id)
    if deleted_packaging_type:
        return jsonify(deleted_packaging_type.to_dict())
    return jsonify({'message': 'Packaging Type not found'}), 404


# Segement ***************************************************

@app.route('/segments', methods=['GET'])
def get_segments():
    segments = SegmentService.get_all_segments()
    return jsonify([segment.to_dict() for segment in segments])


@app.route('/segments/<int:segment_id>', methods=['GET'])
def get_segment(segment_id):
    segment = SegmentService.get_segment_by_id(segment_id)
    if segment:
        return jsonify(segment.to_dict())
    return jsonify({'message': 'Segment not found'}), 404


@app.route('/segments', methods=['POST'])
def create_segment():
    data = request.get_json()
    name = data.get('name')
    project_id = data.get('project_id')
    sum_of_hc_of_lines = data.get('sum_of_hc_of_lines')
    new_segment = SegmentService.create_segment(name, project_id, sum_of_hc_of_lines)
    return jsonify(new_segment.to_dict()), 201


@app.route('/segments/<int:segment_id>', methods=['PUT'])
def update_segment(segment_id):
    data = request.get_json()
    name = data.get('name')
    project_id = data.get('project_id')
    sum_of_hc_of_lines = data.get('sum_of_hc_of_lines')
    updated_segment = SegmentService.update_segment(segment_id, name, project_id, sum_of_hc_of_lines)
    if updated_segment:
        return jsonify(updated_segment.to_dict())
    return jsonify({'message': 'Segment not found'}), 404


@app.route('/segments/<int:segment_id>', methods=['DELETE'])
def delete_segment(segment_id):
    result = SegmentService.delete_segment(segment_id)
    if result:
        return jsonify({'message': 'Segment deleted successfully'})
    return jsonify({'message': 'Segment not found'}), 404


# group Routes *********************************

@app.route('/groups', methods=['POST'])
def create_group():
    data = request.json
    name = data.get('name')
    production_line = data.get('production_line')

    group = GroupService.create(name, production_line)
    return jsonify({'message': 'Group created successfully', 'group': group.to_dict()}), 201


@app.route('/groups', methods=['GET'])
def get_all_groups():
    groups = GroupService.get_all()
    return jsonify([group.to_dict() for group in groups]), 200


@app.route('/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group = GroupService.get_by_id(group_id)
    if group:
        return jsonify(group.to_dict()), 200
    return jsonify({'error': 'Group not found'}), 404


@app.route('/groups/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    data = request.json
    name = data.get('name')
    production_line = data.get('production_line')

    group = GroupService.update(group_id, name, production_line)
    if group:
        return jsonify(group.to_dict()), 200
    return jsonify({'error': 'Group not found'}), 404


@app.route('/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    success = GroupService.delete(group_id)
    if success:
        return jsonify({'message': 'Group deleted successfully'}), 200
    return jsonify({'error': 'Group not found'}), 404


@app.route('/users/<int:user_id>/assign_group', methods=['PUT'])
def assign_group(user_id):
    data = request.json
    group_id = data.get('group_id')

    user = UserService.assign_group(user_id, group_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'User or Group not found'}), 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)
