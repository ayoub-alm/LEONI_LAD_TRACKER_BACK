from database import db
from models.post import Post


class PostService:
    @staticmethod
    def create_post(name):
        post = Post(name=name)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def get_post_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def update_post(post_id, name=None):
        post = Post.query.get(post_id)
        if post:
            if name is not None:
                post.name = name
            db.session.commit()
        return post

    @staticmethod
    def delete_post(post_id):
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
        return post

    @staticmethod
    def get_all_posts():
        return Post.query.all()
