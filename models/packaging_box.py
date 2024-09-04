from database import db
from models.base_model import BaseModel


class PackagingBox(BaseModel, db.Model):
    __tablename__ = 'packaging_boxs'
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Integer, db.ForeignKey('production_lines.id'))
    to_be_delivered_quantity = db.Column(db.Integer)
    delivered_quantity = db.Column(db.Integer, default=0)
    harness_id = db.Column(db.Integer , db.ForeignKey('harnesses.id'), nullable=True)
    status = db.Column(db.String(50))
    barcode = db.Column(db.String(100), unique=True)

    line = db.relationship('ProductionLine', back_populates='packaging_boxes')
    prod_harness = db.relationship('ProdHarness', back_populates='packaging_box', lazy='dynamic')
    harness = db.relationship('HarnessModel')

    def __init__(self, line_id, to_be_delivered_quantity, delivered_quantity, harness_id, status, created_by, barcode):
        super().__init__()
        self.line_id = line_id
        self.to_be_delivered_quantity = to_be_delivered_quantity
        self.delivered_quantity = delivered_quantity
        self.harness_id = harness_id
        self.status = status
        self.barcode = barcode
        self.created_by = created_by

    def to_dict(self):
        return {
            'id': self.id,
            'line_id': self.line_id,
            'to_be_delivered_quantity': self.to_be_delivered_quantity,
            'delivered_quantity': self.delivered_quantity,
            'harness_id': self.harness_id,
            'status': self.status,
            'created_by': self.created_by,
            'barcode': self.barcode,
            'line': self.line.to_dict() if self.line is not None else None,
            'prod_harness': [harness.to_dict() for harness in self.prod_harness],
            'harness': self.harness.to_dict()
        }
