from flask import jsonify

from database import db
from models.prod_harness import ProdHarness
from services.production_job_service import ProductionJobService

class ProdHarnessService:
    @staticmethod
    def create(uuid, box_number, range_time, production_job_id):
        prod_harness = ProdHarness(uuid=uuid, box_number=box_number, range_time=range_time,
                                   production_job_id=production_job_id)
        # update the delivered quantity in production job
        production_job = ProductionJobService.get_by_id(production_job_id)
        status = 0
        delivered_quantity = production_job.delivered_quantity + 1
        if delivered_quantity < production_job.demanded_quantity:
            ProductionJobService.update(production_job_id, None, None, None, None,
                                        production_job.delivered_quantity + 1, status)

        if delivered_quantity == production_job.demanded_quantity:
            status = 1
            ProductionJobService.update(production_job_id, None, None, None, None,
                                        production_job.delivered_quantity + 1 , status)

        db.session.add(prod_harness)
        db.session.commit()
        return prod_harness

    @staticmethod
    def get_by_id(prod_harness_id):
        return ProdHarness.query.get(prod_harness_id)

    @staticmethod
    def update(prod_harness_id, uuid=None, box_number=None, range_time=None, production_job_id=None):
        try:
            prod_harness = ProdHarnessService.get_by_id(prod_harness_id)
            if prod_harness:
                if uuid is not None:
                    prod_harness.uuid = uuid
                if box_number is not None:
                    prod_harness.box_number = box_number
                if range_time is not None:
                    prod_harness.range_time = range_time
                if production_job_id is not None:
                    prod_harness.production_job_id = production_job_id

                db.session.commit()
                return prod_harness
            else:
                return None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(prod_harness_id):
        try:
            prod_harness = ProdHarnessService.get_by_id(prod_harness_id)
            if prod_harness:
                db.session.delete(prod_harness)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        harnesses = ProdHarness.query.all()
        return harnesses
