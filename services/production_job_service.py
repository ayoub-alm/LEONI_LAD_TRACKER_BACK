import random

from database import db
from models.production_job import ProductionJob


class ProductionJobService:

    @staticmethod
    def create(line_id, harness_id, demanded_quantity=0, delivered_quantity=0):
        # generate a unique number
        ref = ''.join([str(random.randint(0, 9)) for _ in range(8)])

        production_job = ProductionJob(ref, line_id, harness_id, demanded_quantity,
                                       delivered_quantity, 0)
        db.session.add(production_job)
        db.session.commit()
        return production_job

    @staticmethod
    def get_by_id(production_job_id):
        return ProductionJob.query.get(production_job_id)

    @staticmethod
    def get_current_production_job_by_line(production_line_id):
        return ProductionJob.query.filter_by(production_line_id=production_line_id, status=0).first()

    @staticmethod
    def get_awaiting_production_job_by_line(production_line_id):
        return ProductionJob.query.filter_by(production_line_id=production_line_id, status=0)

    @staticmethod
    def update(production_job_id, ref=None, production_line_id=None, harness_id=None, demanded_quantity=None,
               delivered_quantity=None, status=None):
        try:
            production_job = ProductionJobService.get_by_id(production_job_id)
            if production_job:
                if ref is not None:
                    production_job.ref = ref
                if production_line_id is not None:
                    production_job.production_line_id = production_line_id
                if harness_id is not None:
                    production_job.harness_id = harness_id
                if demanded_quantity is not None:
                    production_job.demanded_quantity = demanded_quantity
                if delivered_quantity is not None:
                    production_job.delivered_quantity = delivered_quantity
                if status is not None:
                    production_job.status = status

                db.session.commit()
                return production_job
            else:
                return None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(production_job_id):
        try:
            production_job = ProductionJobService.get_by_id(production_job_id)
            if production_job:
                db.session.delete(production_job)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        return ProductionJob.query.all()
