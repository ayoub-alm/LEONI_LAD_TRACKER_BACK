from database import db
from models.field import Field

class FieldService:
    @staticmethod
    def create_field(name, pre_fix):
        field = Field(name=name, pre_fix=pre_fix)
        db.session.add(field)
        db.session.commit()
        return field

    @staticmethod
    def get_field_by_id(field_id):
        return Field.query.get(field_id)

    @staticmethod
    def update_field(field_id, name=None, pre_fix=None):
        field = Field.query.get(field_id)
        if field:
            if name is not None:
                field.name = name
            if pre_fix is not None:
                field.pre_fix = pre_fix
            db.session.commit()
        return field

    @staticmethod
    def delete_field(field_id):
        field = Field.query.get(field_id)
        if field:
            db.session.delete(field)
            db.session.commit()
        return field

    @staticmethod
    def get_all_fields():
        return Field.query.all()
