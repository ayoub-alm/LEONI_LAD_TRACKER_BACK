from database import db
from models.production_line import ProductionLine
from flask import jsonify

class ProductionLineService:
    @staticmethod
    def create_production_line(name, project_id):
        production_line = ProductionLine(name=name, project_id=project_id)
        db.session.add(production_line)
        db.session.commit()
        return production_line

    @staticmethod
    def get_production_line_by_id(production_line_id):
        return ProductionLine.query.get(production_line_id)

    @staticmethod
    def get_all_production_lines():
        lines = ProductionLine.query.all()
        lines_dict = [line.to_dict() for line in lines]
        return jsonify(lines_dict)
