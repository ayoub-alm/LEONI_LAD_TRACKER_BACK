# services/packaging_type_service.py
from models.packaging_type import PackagingType
from database import db


class PackagingTypeService:
    @staticmethod
    def create_packaging_type(type, size, weight):
        new_packaging_type = PackagingType(type=type, size=size, weight=weight)
        db.session.add(new_packaging_type)
        db.session.commit()
        return new_packaging_type

    @staticmethod
    def get_packaging_type_by_id(packaging_type_id):
        return PackagingType.query.get(packaging_type_id)

    @staticmethod
    def get_all_packaging_types():
        return PackagingType.query.all()

    @staticmethod
    def update_packaging_type(packaging_type_id, type=None, size=None, weight=None):
        packaging_type = PackagingType.query.get(packaging_type_id)
        if packaging_type:
            if type is not None:
                packaging_type.type = type
            if size is not None:
                packaging_type.size = size
            if weight is not None:
                packaging_type.weight = weight
            db.session.commit()
        return packaging_type

    @staticmethod
    def delete_packaging_type(packaging_type_id):
        packaging_type = PackagingType.query.get(packaging_type_id)
        if packaging_type:
            db.session.delete(packaging_type)
            db.session.commit()
        return packaging_type
