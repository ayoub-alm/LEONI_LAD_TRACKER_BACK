from datetime import datetime

from flask import jsonify
from database import db
from models.packaging_box import PackagingBox
from models.prod_harness import ProdHarness
from services.production_job_service import ProductionJobService


class ProdHarnessService:
    @staticmethod
    def create(uuid, box_number, range_time, production_job_id, status=0, packaging_box_id=None):
        try:
            exists = ProdHarnessService.prod_harness_exists(uuid)
            if exists:
                return None
            else:
                prod_harness = ProdHarness(
                    uuid=uuid,
                    box_number=box_number,
                    range_time=range_time,
                    production_job_id=production_job_id,
                    status=status,
                    packaging_box_id=packaging_box_id
                )
                db.session.add(prod_harness)
                if packaging_box_id:
                    packaging_box = PackagingBox.query.filter_by(id=packaging_box_id).first()
                    if packaging_box:
                        packaging_box.delivered_quantity += 1
                        if packaging_box.to_be_delivered_quantity == packaging_box.delivered_quantity:
                            packaging_box.status = 2
                db.session.commit()
                return prod_harness
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by_id(prod_harness_id):
        return ProdHarness.query.get(prod_harness_id)

    @staticmethod
    def update(prod_harness_id, uuid=None, box_number=None, range_time=None, production_job_id=None, status=None,
               packaging_box_id=None):
        try:
            prod_harness = ProdHarnessService.get_by_id(prod_harness_id)
            if prod_harness:
                if uuid is not None:
                    prod_harness.uuid = uuid
                if box_number is not None:
                    prod_harness.box_number = box_number
                if range_time is not None:
                    prod_harness.range_time = range_time
                else:
                    created_at = prod_harness.created_at
                    now = datetime.utcnow()
                    range_time = (now - created_at).total_seconds() / 60
                    prod_harness.range_time = range_time
                if production_job_id is not None:
                    prod_harness.production_job_id = production_job_id
                if status is not None:
                    prod_harness.status = status
                if packaging_box_id is not None:
                    prod_harness.packaging_box_id = packaging_box_id

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
        return ProdHarness.query.all()

    @staticmethod
    def get_by_uuid(uuid):
        return ProdHarness.query.filter_by(uuid=uuid).first()

    def prod_harness_exists(uuid: str) -> bool:
        """
        Checks if a ProdHarness record exists based on the provided uuid.

        :param uuid: The unique identifier of the ProdHarness.
        :return: True if the record exists, False otherwise.
        """
        return db.session.query(ProdHarness).filter_by(uuid=uuid).first() is not None
