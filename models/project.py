from database import db

from models.base_model import BaseModel


class Project(BaseModel, db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ref = db.Column(db.String(50), unique=True)
    segments = db.relationship('Segment', back_populates='project')

    def __init__(self, name, ref):
        super().__init__()
        self.name = name
        self.ref = ref

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ref': self.ref,
            'segments': self.segments if self.segments else None
        }
