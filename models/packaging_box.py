from database import db
from models.base_model import BaseModel


class PackagingBox(BaseModel,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Integer, db.ForeignKey('production_line.id'))
    quantity = db.Column(db.Integer)
    harness_id = db.Column(db.Integer)
    status = db.Column(db.String(50))
    barcode = db.Column(db.String(100))

    def __init__(self, line_id, quantity, harness_id, status, created_by, barcode):
        super().__init__()
        self.line_id = line_id
        self.quantity = quantity
        self.harness_id = harness_id
        self.status = status
        self.created_by = created_by
        self.barcode = barcode

    def to_dict(self):
        return {
            'id': self.id,
            'line_id': self.line_id,
            'quantity': self.quantity,
            'harness_id': self.harness_id,
            'status': self.status,
            'created_by': self.created_by,
            'barcode': self.barcode
        }
