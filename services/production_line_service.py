from database import db
from models.production_line import ProductionLine


class ProductionLineService:

    @staticmethod
    def create(name, number_of_operators=0, project_id=None):
        production_line = ProductionLine(name=name, number_of_operators=number_of_operators, project_id=project_id)
        db.session.add(production_line)
        db.session.commit()
        return production_line

    @staticmethod
    def get_by_id(production_line_id):
        return ProductionLine.query.get(production_line_id)

    @staticmethod
    def update(production_line_id, name=None, number_of_operators=None, project_id=None):
        try:
            production_line = ProductionLineService.get_by_id(production_line_id)
            if production_line:
                if name is not None:
                    production_line.name = name
                if number_of_operators is not None:
                    production_line.number_of_operators = number_of_operators
                if project_id is not None:
                    production_line.project_id = project_id

                db.session.commit()
                return production_line
            else:
                return None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(production_line_id):
        try:
            production_line = ProductionLineService.get_by_id(production_line_id)
            if production_line:
                db.session.delete(production_line)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            db.session.rollback()
            raise e
    @staticmethod
    def get_all_production_lines():
        return ProductionLine.query.all()