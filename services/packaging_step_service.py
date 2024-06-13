from database import db
from models.packaging_step import PackagingStep
from typing import List


class PackagingStepService:
    @staticmethod
    def create_packaging_step(pre_fix, field, status, description, packaging_process_id, img, order):
        step = PackagingStep(pre_fix=pre_fix, field_id=field, status=status, description=description,
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

    @staticmethod
    def create_bulk_packaging_steps(steps: List[dict]):
        step_objects = []
        for step_data in steps:
            step = PackagingStep(
                pre_fix=step_data.get('preFix'),
                field_id=step_data.get('fieldId'),
                status=step_data.get('status'),
                description=step_data.get('description'),
                packaging_process_id=step_data.get('packagingProcessId'),
                img=step_data.get('img'),
                order=step_data.get('order'),
                name=step_data.get('name', ''),
                next_step_on_success=step_data.get('next_step_on_success'),
                next_step_on_failure=step_data.get('next_step_on_failure'),
                condition=step_data.get('condition', False)
            )
            step_objects.append(step)
            db.session.add(step)

        db.session.commit()
        return step_objects
