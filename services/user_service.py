from models.user import User
from database import db

class UserService:

    @staticmethod
    def create_user(username, password, role, matriculate):
        new_user = User(username=username, password=password, role=role, matriculate=matriculate)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def update_user(user_id, username=None, password=None, role=None, matriculate=None):
        user = User.query.get(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if password:
            user.password = password
        if role:
            user.role = role
        if matriculate:
            user.matriculate = matriculate
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        db.session.delete(user)
        db.session.commit()
        return user
