from models.base_model import BaseModel
from database import db


class PackagingType(BaseModel, db.Model):
    __tablename__ = 'packaging_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), unique=True, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __init__(self, type, size, weight):
        super().__init__()
        self.type = type
        self.size = size
        self.weight = weight

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'size': self.size,
            'weight': self.weight
        }
