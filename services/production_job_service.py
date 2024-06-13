import random

from sqlalchemy import and_

from database import db
from models.production_job import ProductionJob


class ProductionJobService:

    @staticmethod
    def create(line_id, harness_id, demanded_quantity=0, delivered_quantity=0):
        # generate a unique number
        ref = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        last_created_job_order = (ProductionJob.query.filter_by(production_line_id=line_id, status=0)
                                  .order_by(ProductionJob.order.desc()).first())
        if last_created_job_order is None:
            production_job = ProductionJob(ref, line_id, harness_id, demanded_quantity,
                                           delivered_quantity, 0, 1)
        else:
            production_job = ProductionJob(ref, line_id, harness_id, demanded_quantity,
                                           delivered_quantity, 0, last_created_job_order.order + 1)
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

    @staticmethod
    def re_order(production_line_id, job_id, desc_or_asd):
        production_jobs = ProductionJob.query.filter_by(production_line_id=production_line_id, status=0).all()
        production_jobs.sort()


class ProductionJobManager:
    @staticmethod
    def re_order(job_id, desc_or_asd):
        selected_production_job = ProductionJob.query.filter_by(id=job_id, status=0).first()
        # production_jobs = ProductionJob.query.filter_by(production_line=job_id, status=0).all()
        if desc_or_asd.lower() == 'desc':
            selected_production_job.order = selected_production_job.order - 1
            production_jobs = ProductionJob.query.filter_by(
                and_(
                    ProductionJob.production_line_id == selected_production_job.production_line_id,
                    ProductionJob.status == 0,
                    ProductionJob.order < selected_production_job.order
                )
            ).all()
            for selected_production_job in production_jobs:
                selected_production_job.order = selected_production_job.order - 1
        elif desc_or_asd.lower() == 'desc':
            selected_production_job.order = selected_production_job.order + 1
            production_jobs = ProductionJob.query.filter_by(
                and_(
                    ProductionJob.production_line_id == selected_production_job.production_line_id,
                    ProductionJob.status == 0,
                    ProductionJob.order > selected_production_job.order
                )
            ).all()
            for selected_production_job in production_jobs:
                selected_production_job.order = selected_production_job.order + 1
        else:
            raise ValueError("Invalid sorting order. Use 'asc' for ascending or 'desc' for descending.")
        return production_jobs

# Example usage
# production_jobs = ProductionJobManager.re_order(production_line_id, job_id, 'asc')
