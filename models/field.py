from sqlalchemy.orm import relationship

from database import db
from models.base_model import BaseModel


class Field(BaseModel, db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, id, name ) -> None:
        super().__init__()
        # self.post_id = post_id
        # self.pre_fix = pre_fix
        self.name = name
        self.id = id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            # 'pre_fix': self.pre_fix,
            # 'posts': [post.to_dict() for post in self.posts]
        }
