from database import db
from models.base_model import BaseModel


class PackagingProcess(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    family = db.Column(db.String(50))
    status = db.Column(db.Integer, default=1)
    name = db.Column(db.String(50))
    steps = db.relationship('PackagingStep', backref='packaging_process', lazy=True)

    def __init__(self, family, status, name):   
        super().__init__()
        self.family = family
        self.status = status
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'family': self.family,
            'status': self.status,
            'name': self.name,
            'steps': [step.to_dict() for step in self.steps]  # Include steps in the dictionary representation
        }
