from database import db
from models.base_model import BaseModel


class Group(BaseModel, db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    production_line_id = db.Column(db.Integer, db.ForeignKey('production_lines.id'), nullable=True)
    # One-to-many relationship with User
    production_line = db.relationship('ProductionLine', back_populates='groups', lazy=True)

    def __init__(self, name, production_line_id):
        super().__init__()
        self.name = name
        self.production_line_id = production_line_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'production_line': self.production_line.to_dict() if self.production_line else None,
            'users': [user.to_dict() for user in self.users]
        }
