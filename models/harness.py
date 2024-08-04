from database import db
from models.base_model import BaseModel


class HarnessModel(BaseModel, db.Model):
    __tablename__ = 'harnesses'
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(50), nullable=False)
    cpn = db.Column(db.String(50), nullable=False)
    fuse_box = db.Column(db.String(50))
    range_time = db.Column(db.Float)
    package_type_id = db.Column(db.Integer, db.ForeignKey('packaging_types.id'))
    segment_id = db.Column(db.Integer, db.ForeignKey('segments.id'))

    # Define the relationships
    package = db.relationship('PackagingType')
    segment = db.relationship('Segment')

    def __init__(self, ref, cpn, fuse_box, range_time, package_type_id, segment_id):
        super().__init__()
        self.ref = ref
        self.cpn = cpn
        self.fuse_box = fuse_box
        self.range_time = range_time
        self.package_type_id = package_type_id
        self.segment_id = segment_id

    def to_dict(self):
        package = self.package.to_dict() if self.package else None
        segment = self.segment.to_dict() if self.segment else None
        return {
            'id': self.id,
            'ref': self.ref,
            'fuse_box': self.fuse_box,
            'cpn': self.cpn,
            'range_time': self.range_time,
            'package': package,
            'segment': segment
        }
