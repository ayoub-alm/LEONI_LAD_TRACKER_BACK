from sqlalchemy import func

from database import db
from models.harness import HarnessModel


class HarnessService:

    @staticmethod
    def create(ref, fase_iso, family, range_time, project_id):
        try:
            harness = HarnessModel(ref=ref, fase_iso=fase_iso, family=family, range_time=range_time,
                                   project_id=project_id)
            db.session.add(harness)
            db.session.commit()
            return harness
        except Exception as e:
            db.session.rollback()
            raise e
            return 'error'

    @staticmethod
    def get_by_id(harness_id):
        return HarnessModel.query.get(harness_id)

    @staticmethod
    def update(harness_id, ref=None, fase_iso=None, family=None, range_time=None, project_id=None):
        try:
            harness = HarnessService.get_by_id(harness_id)
            if harness:
                if ref is not None:
                    harness.ref = ref
                if fase_iso is not None:
                    harness.fuse_box = fase_iso
                if family is not None:
                    harness.family = family
                if range_time is not None:
                    harness.range_time = range_time
                if project_id is not None:
                    harness.project_id = project_id

                db.session.commit()
                return harness
            else:
                return None  # or raise an exception indicating the harness was not found
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(harness_id):
        try:
            harness = HarnessService.get_by_id(harness_id)
            if harness:
                db.session.delete(harness)
                db.session.commit()
                return True
            else:
                return False  # or raise an exception indicating the harness was not found
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        return HarnessModel.query.all()

    @staticmethod
    def get_families():
        return db.session.query(HarnessModel.id, HarnessModel.family, func.count()).group_by(HarnessModel.family).all()

    @staticmethod
    def get_by_ref(ref):
        return HarnessModel.query.filter_by(ref=ref).all()
