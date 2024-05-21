from database import db
from models.packaging_step import PackagingStep


class PackagingStepService:
    @staticmethod
    def create_packaging_step(pre_fix, field, status, description, packaging_process_id, img, order):
        step = PackagingStep(pre_fix=pre_fix, field=field, status=status, description=description,
                             packaging_process_id=packaging_process_id, img=img, order=order)
        db.session.add(step)
        db.session.commit()
        return step

    @staticmethod
    def get_step_by_id(step_id):
        return PackagingStep.query.get(step_id)

    @staticmethod
    def update_packaging_step(step_id, pre_fix=None, field=None, status=None, description=None, img=None, order=None):
        step = PackagingStep.query.get(step_id)
        if step:
            if pre_fix is not None:
                step.pre_fix = pre_fix
            if field is not None:
                step.field = field
            if status is not None:
                step.status = status
            if description is not None:
                step.description = description
            if img is not None:
                step.img = img
            if order is not None:
                step.order = order
            db.session.commit()
        return step

    @staticmethod
    def delete_packaging_step(step_id):
        step = PackagingStep.query.get(step_id)
        if step:
            db.session.delete(step)
            db.session.commit()
        return step

    @staticmethod
    def get_all_steps():
        return PackagingStep.query.all()
