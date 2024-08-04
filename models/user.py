from database import db
from models.base_model import BaseModel


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    matriculate = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(20), default='user')
    created_harnesses = db.relationship('HarnessModel', backref='creator', lazy=True)

    def __init__(self, username, password, role, matriculate):
        super().__init__()
        self.username = username
        self.password = password
        self.role = role
        self.matriculate = matriculate

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'matriculate': self.matriculate,
            'role': self.role,
        }
