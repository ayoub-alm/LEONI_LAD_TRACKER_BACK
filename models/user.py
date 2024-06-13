from database import db
from models.base_model import BaseModel


class User(BaseModel, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(20), default='user')

    def __init__(self, username, password, role):
        super().__init__()
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }