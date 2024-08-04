from database import db
from models.packaging_process import PackagingProcess


class PackagingProcessService:
    @staticmethod
    def create_process(segmentId, status, name):
        process = PackagingProcess(segment_id=segmentId, status=status, name=name)
        db.session.add(process)
        db.session.commit()
        return process

    @staticmethod
    def get_process_by_id(process_id):
        return PackagingProcess.query.get(process_id)

    @staticmethod
    def update_process(process_id, family_id=None, status=None, name=None):
        process = PackagingProcess.query.get(process_id)
        if process:
            if family_id is not None:
                process.family_id = family_id
            if status is not None:
                process.status = status
            if name is not None:
                process.name = name
            db.session.commit()
        return process

    @staticmethod
    def delete_process(process_id):
        process = PackagingProcess.query.get(process_id)
        if process:
            db.session.delete(process)
            db.session.commit()
        return process

    @staticmethod
    def get_all_processes():
        return PackagingProcess.query.all()

    @staticmethod
    def get_process_by_segment_id(segment_id):
        return PackagingProcess.query.filter(PackagingProcess.segment_id == segment_id).first()
