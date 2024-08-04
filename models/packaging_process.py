from database import db
from models.base_model import BaseModel

class PackagingProcess(BaseModel, db.Model):
    __tablename__ = 'packaging_processes'
    id = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer, db.ForeignKey('segments.id'), nullable=False)  # Foreign key to Segment
    status = db.Column(db.Integer, default=1)
    name = db.Column(db.String(50))
    segment = db.relationship('Segment', backref='packaging_processes', lazy=True)  # Ensure backref is unique
    steps = db.relationship('PackagingStep', backref='packaging_process', lazy=True)

    def __init__(self, segment_id, status, name):
        super().__init__()
        self.segment_id = segment_id
        self.status = status
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'segment_id': self.segment_id,
            'status': self.status,
            'name': self.name,
            'segment':self.segment.to_dict() if self.segment else None,
            'steps': [step.to_dict() for step in self.steps]
        }
