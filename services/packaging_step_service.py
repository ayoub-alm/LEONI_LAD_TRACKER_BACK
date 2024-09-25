import logging
import base64
import os
from werkzeug.utils import secure_filename
from models.packaging_step import PackagingStep
from database import db
from typing import List
from flask import current_app

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class PackagingStepService:
    IMAGE_DIRECTORY = 'static/images'

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
    def save_image(base64_image, filename):
        # Ensure the directory exists
        image_dir = os.path.join(current_app.root_path, PackagingStepService.IMAGE_DIRECTORY)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        try:
            # Decode the base64 string
            image_data = base64.b64decode(base64_image)
            file_path = os.path.join(image_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(image_data)

            # Return a URL path relative to the static folder
            return os.path.join(PackagingStepService.IMAGE_DIRECTORY, filename)
        except Exception as e:
            logging.error(f"Error saving image: {e}")
            return None

    @staticmethod
    def save_image(base64_image: str, filename: str) -> str:
        # Decode the base64 image
        header, base64_data = base64_image.split(',', 1)
        image_data = base64.b64decode(base64_data)

        # Save the image to a file
        img_folder = os.path.join(os.getcwd(), 'static', 'images')
        os.makedirs(img_folder, exist_ok=True)
        img_path = os.path.join(img_folder, filename)

        with open(img_path, 'wb') as f:
            f.write(image_data)

        # Return the relative path to the image
        return f"http://localhost:5000/static/images/{filename}"

    @staticmethod
    def create_bulk_packaging_steps(steps: List[dict]):
        step_objects = []

        for step_data in steps:
            img_path = None
            if 'img' in step_data and step_data['img']:
                base64_image = step_data['img']
                filename = secure_filename(
                    f"{step_data.get('name', 'image')}.png")  # Assuming .png format for the image
                img_path = PackagingStepService.save_image(base64_image, filename)

            step = PackagingStep(
                pre_fix=step_data.get('preFix'),
                field_id=step_data.get('fieldId'),
                status=step_data.get('status'),
                description=step_data.get('description'),
                packaging_process_id=step_data.get('packagingProcessId'),
                img=img_path,
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
