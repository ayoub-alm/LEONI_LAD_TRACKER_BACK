from models.packaging_box import PackagingBox
from database import db

class PackagingBoxService:
    @staticmethod
    def create_packaging_box(line_id, to_be_delivered_quantity, delivered_quantity, harness_id, status, created_by, barcode):
        packaging_box = PackagingBox(line_id=line_id, to_be_delivered_quantity=to_be_delivered_quantity,
                                     delivered_quantity=delivered_quantity, harness_id=harness_id,
                                     status=status, created_by=created_by, barcode=barcode)
        db.session.add(packaging_box)
        db.session.commit()
        return packaging_box

    @staticmethod
    def get_packaging_box_by_id(box_id):
        return PackagingBox.query.get(box_id)

    @staticmethod
    def update_packaging_box(box_id, line_id=None, to_be_delivered_quantity=None, delivered_quantity=None, harness_id=None, status=None, created_by=None, barcode=None):
        packaging_box = PackagingBoxService.get_packaging_box_by_id(box_id)
        if packaging_box:
            if line_id is not None:
                packaging_box.line_id = line_id
            if to_be_delivered_quantity is not None:
                packaging_box.to_be_delivered_quantity = to_be_delivered_quantity
            if delivered_quantity is not None:
                packaging_box.delivered_quantity = delivered_quantity
            if harness_id is not None:
                packaging_box.harness_id = harness_id
            if status is not None:
                packaging_box.status = status
            if created_by is not None:
                packaging_box.created_by = created_by
            if barcode is not None:
                packaging_box.barcode = barcode
            db.session.commit()
        return packaging_box

    @staticmethod
    def delete_packaging_box(box_id):
        packaging_box = PackagingBoxService.get_packaging_box_by_id(box_id)
        if packaging_box:
            db.session.delete(packaging_box)
            db.session.commit()
        return packaging_box

    @staticmethod
    def get_all_packaging_boxes():
        return PackagingBox.query.all()

    @staticmethod
    def get_opened_package(line_id):
        return PackagingBox.query.filter_by(line_id=line_id, status=0).first()
