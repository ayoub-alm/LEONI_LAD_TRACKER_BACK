from sqlalchemy.orm import relationship
from database import db
from models.base_model import BaseModel
from models.production_job import ProductionJob
from models.packaging_box import PackagingBox  # Assuming this model exists


class ProdHarness(BaseModel, db.Model):
    __tablename__ = 'prod_harnesses'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50), unique=True)
    box_number = db.Column(db.String(50), nullable=True)
    range_time = db.Column(db.Float, nullable=True)
    production_job_id = db.Column(db.Integer, db.ForeignKey('production_jobs.id'), nullable=True)
    status = db.Column(db.Integer, default=1)
    packaging_box_id = db.Column(db.Integer, db.ForeignKey('packaging_boxs.id'), nullable=True)

    production_job = db.relationship('ProductionJob', backref='prod_harness', lazy=True)
    packaging_box = db.relationship('PackagingBox', back_populates='prod_harness', lazy=True)

    def __init__(self, uuid, box_number, range_time, production_job_id, status, packaging_box_id):
        super().__init__()
        self.uuid = uuid
        self.box_number = box_number
        self.range_time = range_time
        self.production_job_id = production_job_id
        self.status = status
        self.packaging_box_id = packaging_box_id

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'box_number': self.box_number,
            'range_time': self.range_time,
            'production_job': self.production_job.to_dict() if self.production_job else None,
            'status': self.status,
            'packaging_box_id': self.packaging_box_id,
            'created_at': self.created_at
        }
