from database import db
from models.base_model import BaseModel


class ProductionLine(BaseModel, db.Model):
    __tablename__ = 'production_lines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    number_of_operators = db.Column(db.Integer, default=0)
    segment_id = db.Column(db.Integer, db.ForeignKey('segments.id'))
    packaging_boxes = db.relationship('PackagingBox', back_populates='line', lazy='dynamic')
    groups = db.relationship('Group', back_populates='production_line', lazy='dynamic')

    def __init__(self, id, name, number_of_operators, segment_id):
        super().__init__()
        self.id = id,
        self.name = name
        self.number_of_operators = number_of_operators
        self.segment_id = segment_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'number_of_operators': self.number_of_operators,
            'segment_id': self.segment_id
        }
