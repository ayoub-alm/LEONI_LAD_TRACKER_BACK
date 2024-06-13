from sqlalchemy.orm import relationship

from database import db
from models.base_model import BaseModel


class ProdHarness(BaseModel, db.Model):
    __tablename__ = 'prod_harness'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50))
    box_number = db.Column(db.String(50), nullable=True)
    range_time = db.Column(db.Float, nullable=True)
    production_job_id = db.Column(db.Integer, db.ForeignKey('production_job.id'))
    production_job = db.relationship('ProductionJob', backref='prod_harness', lazy=True)
    status = db.Column(db.Integer,  default=1)
    packaging_box_id = db.Column(db.Integer,  db.ForeignKey('packaging_box.id'), nullable=True)

    def __init__(self, uuid, box_number=None, range_time=None, production_job_id=None):
        super().__init__()
        self.uuid = uuid
        self.box_number = box_number
        self.range_time = range_time
        self.production_job_id = production_job_id

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'box_number': self.box_number,
            'range_time': self.range_time,
            'production_job': self.production_job.to_dict()
        }
