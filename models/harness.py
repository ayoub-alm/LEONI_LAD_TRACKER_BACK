from database import db
from models.base_model import BaseModel
from models.project import Project


class HarnessModel(BaseModel, db.Model):
    __tablename__ = 'harness'
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(50))
    fuse_box = db.Column(db.String(50))
    family = db.Column(db.String(50))
    range_time = db.Column(db.Float)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self) -> None:
        super().__init__()

    def to_dict(self):
        project = Project.query.get(self.project_id).to_dict()
        return {
            'id': self.id,
            'ref': self.ref,
            'fuse_box': self.fuse_box,
            'family': self.family,
            'range_time': self.range_time,
            'project_id': self.project_id,
            'project': project
        }
