from database import db

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    fields = db.relationship('Field', backref='field', lazy=True)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'fields': [field.to_dict() for field in self.fields]
        }
