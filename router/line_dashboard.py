from flask import Blueprint, request, jsonify
import pyodbc
from datetime import datetime

from database import db
from models.harness import HarnessModel
from models.packaging_box import PackagingBox

line_dashboard_bp = Blueprint('line_dashboard_bp', __name__)


# Function to get database connection
def get_db_connection():
    conn = pyodbc.connect(
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=./db.accdb;'
    )
    return conn


line_dashboard_bp = Blueprint('line_dashboard_bp', __name__)


# Function to apply filters to queries
def apply_filters(query, filters):
    from_date = filters.get('from')
    to_date = filters.get('to')
    shift = filters.get('shift')

    if not from_date:
        from_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not to_date:
        to_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = query.filter(PackagingBox.updated_at.between(from_date, to_date))

    shifts_to_include = []
    if shift:
        shifts_to_include.append(shift)
    else:
        shifts_to_include = ['a', 'b', 'c']

    shift_conditions = []
    for shift in shifts_to_include:
        if shift == 'a':
            shift_conditions.append(db.text("HOUR(updated_at) BETWEEN 6 AND 14"))
        elif shift == 'b':
            shift_conditions.append(db.text("HOUR(updated_at) BETWEEN 14 AND 22"))
        elif shift == 'c':
            shift_conditions.append(
                db.text("(HOUR(updated_at) BETWEEN 22 AND 23) OR (HOUR(updated_at) BETWEEN 0 AND 6)"))

    if shift_conditions:
        query = query.filter(db.or_(*shift_conditions))

    return query


@line_dashboard_bp.route('/api/line-dashboard/total-quantity', methods=['POST'])
def total_quantity():
    try:
        filters = request.json
        query = db.session.query(db.func.sum(PackagingBox.delivered_quantity).label('total_quantity'))
        query = apply_filters(query, filters)
        result = query.one()
        return jsonify({'total_quantity': result.total_quantity})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/average-quantity', methods=['POST'])
def average_quantity():
    try:
        filters = request.json
        query = db.session.query(db.func.avg(PackagingBox.delivered_quantity).label('average_quantity'))
        query = apply_filters(query, filters)
        result = query.one()
        return jsonify({'average_quantity': result.average_quantity})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/count-by-code-fournisseur', methods=['POST'])
def count_by_code_fournisseur():
    try:
        filters = request.json
        query = db.session.query(
            PackagingBox.harness_id,
            db.func.count(PackagingBox.id).label('box_count'),
            PackagingBox.harness
        ).join(HarnessModel).group_by(PackagingBox.harness_id)
        query = apply_filters(query, filters)
        result = query.all()
        data = [{'code_fournisseur': row.harness.ref, 'box_count': row.box_count} for row in result]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/count-by-hour', methods=['POST'])
def count_by_hour():
    try:
        filters = request.json
        query = db.session.query(
            db.func.hour(PackagingBox.updated_at).label('hour'),
            db.func.count(PackagingBox.barcode).label('box_count')
        ).group_by(db.func.hour(PackagingBox.updated_at))
        query = apply_filters(query, filters)
        result = query.all()
        data = [{'hour': row.hour, 'box_count': row.box_count} for row in result]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/quantity-by-hour', methods=['POST'])
def quantity_by_hour():
    try:
        filters = request.json
        query = db.session.query(
            db.func.hour(PackagingBox.updated_at).label('hour'),
            db.func.sum(PackagingBox.delivered_quantity).label('total_quantity')
        ).group_by(db.func.hour(PackagingBox.updated_at))
        query = apply_filters(query, filters)
        query = query.order_by(db.func.hour(PackagingBox.updated_at))
        result = query.all()
        data = [{'hour': row.hour, 'total_quantity': row.total_quantity} for row in result]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/productive-hours', methods=['POST'])
def productive_hours():
    try:
        filters = request.json
        temps_game = filters.get('temps_game', 0)
        start_time = filters.get('from')
        end_time = filters.get('to')
        vsm = filters.get('vsm')
        if not start_time or not end_time:
            return jsonify({'error': 'start and end times are required'}), 400

        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        total_time = (end_time - start_time).total_seconds() / 3600

        query = db.session.query(db.func.sum(PackagingBox.delivered_quantity).label('total_quantity'))
        query = apply_filters(query, filters)
        result = query.one()

        if len(result) < 1 :
            total_quantity = result.total_quantity or 0
            efficiency = (total_quantity * temps_game) / (vsm * total_time) * 100 if total_time > 0 else 0
            expected = (vsm * total_time) / temps_game if temps_game > 0 else 0

            return jsonify({
                'posted_hours': total_time,
                'productive_hours': 0,
                'total_quantity': 0,
                'efficiency': efficiency,
                'expected': expected
            })

        total_quantity = result.total_quantity or 0
        productive_hours = (total_quantity * temps_game) / vsm if temps_game else 0
        efficiency = (total_quantity * temps_game) / (vsm * total_time) * 100 if total_time > 0 else 0
        expected = (vsm * total_time) / temps_game if temps_game > 0 else 0

        return jsonify({
            'posted_hours': total_time,
            'productive_hours': productive_hours,
            'total_quantity': total_quantity,
            'efficiency': efficiency,
            'expected': expected
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/sum-by-code-fournisseur', methods=['POST'])
def sum_by_code_fournisseur():
    try:
        filters = request.json
        query = db.session.query(
            PackagingBox,
            # PackagingBox.harness.ref.label('ref'),
            db.func.sum(PackagingBox.delivered_quantity).label('total_quantity')
        ).group_by(PackagingBox.harness_id)
        query = apply_filters(query, filters)
        result = query.all()
        data = [{'code_fournisseur': row.PackagingBox.harness.ref, 'total_quantity': row.total_quantity} for row in result]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/total-quantity-current', methods=['POST'])
def total_quantity_current():
    try:
        query = db.session.query(db.func.sum(PackagingBox.to_be_delivered_quantity).label('total_quantity'))
        result = query.one()
        return jsonify({'total_quantity': result.total_quantity})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/quantity-by-date', methods=['POST'])
def quantity_by_date():
    try:
        filters = request.json
        query = db.session.query(
            db.func.date(PackagingBox.updated_at).label('formatted_date'),
            db.func.sum(PackagingBox.delivered_quantity).label('total_quantity')
        ).group_by(db.func.date(PackagingBox.updated_at))
        query = apply_filters(query, filters)
        query = query.order_by(db.func.date(PackagingBox.updated_at))
        result = query.all()
        data = [{'date': row.formatted_date, 'total_quantity': row.total_quantity} for row in result]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@line_dashboard_bp.route('/api/line-dashboard/quantity-by-month', methods=['POST'])
def quantity_by_month():
    try:
        filters = request.json
        query = db.session.query(
            db.func.date_format(PackagingBox.updated_at, '%Y-%m').label('month'),
            db.func.sum(PackagingBox.delivered_quantity).label('total_quantity')
        ).group_by(db.func.date_format(PackagingBox.updated_at, '%Y-%m'))
        query = apply_filters(query, filters)
        query = query.order_by(db.func.date_format(PackagingBox.updated_at, '%Y-%m'))
        result = query.all()
        data = [{'month': row.month, 'total_quantity': row.total_quantity} for row in result]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint to retrieve box count
@line_dashboard_bp.route('/api/line-dashboard/box-count', methods=['POST'])
def box_count():
    try:
        filters = request.json
        query = db.session.query(db.func.count(PackagingBox.id).label('box_count'))
        query = apply_filters(query, filters)
        result = query.one()
        return jsonify({'box_count': result.box_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
