from database import db
from sqlalchemy.orm import relationship

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ref = db.Column(db.String(50), unique=True)
    production_lines = relationship('ProductionLine', backref='project', lazy=True)

    def __init__(self, name, ref):
        self.name = name
        self.ref = ref

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ref': self.ref,
            'production_lines': [production_line.to_dict() for production_line in self.production_lines]
        }
