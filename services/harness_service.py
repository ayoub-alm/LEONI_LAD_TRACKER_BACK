from sqlalchemy import func
from database import db
from models.harness import HarnessModel

class HarnessService:

    @staticmethod
    def create(ref, cpn, fuse_box, range_time, package_type_id, segment_id):
        try:
            harness = HarnessModel(
                ref=ref,
                cpn=cpn,
                fuse_box=fuse_box,
                range_time=range_time,
                package_type_id=package_type_id,
                segment_id=segment_id
            )
            db.session.add(harness)
            db.session.commit()
            return harness
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by_id(harness_id):
        return HarnessModel.query.get(harness_id)

    @staticmethod
    def update(harness_id, ref=None, cpn=None, fuse_box=None, range_time=None, package_type_id=None, segment_id=None):
        try:
            harness = HarnessService.get_by_id(harness_id)
            if harness:
                if ref is not None:
                    harness.ref = ref
                if cpn is not None:
                    harness.cpn = cpn
                if fuse_box is not None:
                    harness.fuse_box = fuse_box
                if range_time is not None:
                    harness.range_time = range_time
                if package_type_id is not None:
                    harness.package_type_id = package_type_id
                if segment_id is not None:
                    harness.segment_id = segment_id

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
        return db.session.query(HarnessModel.family, func.count()).group_by(HarnessModel.family).all()

    @staticmethod
    def get_by_ref(ref):
        return HarnessModel.query.filter_by(ref=ref).all()
