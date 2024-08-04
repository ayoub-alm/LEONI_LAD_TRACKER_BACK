from database import db
from models.group import Group
from models.user import User

class GroupService:

    @staticmethod
    def create(name, production_line):
        try:
            group = Group(name=name, production_line=production_line)
            db.session.add(group)
            db.session.commit()
            return group
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_by_id(group_id):
        return Group.query.get(group_id)

    @staticmethod
    def update(group_id, name=None, production_line=None):
        try:
            group = GroupService.get_by_id(group_id)
            if group:
                if name is not None:
                    group.name = name
                if production_line is not None:
                    group.production_line = production_line
                db.session.commit()
                return group
            return None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(group_id):
        try:
            group = GroupService.get_by_id(group_id)
            if group:
                db.session.delete(group)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        return Group.query.all()

class UserService:

    @staticmethod
    def assign_group(user_id, group_id):
        try:
            user = User.query.get(user_id)
            if user:
                user.group_id = group_id
                db.session.commit()
                return user
            return None
        except Exception as e:
            db.session.rollback()
            raise e
