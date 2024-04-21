import datetime
from typing import Any

from flask import jsonify

import app
from models.user import User
import jwt


class Authentication:
    def __init__(self) -> None:
        super().__init__()

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __format__(self, format_spec: str) -> str:
        return super().__format__(format_spec)

    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            token = jwt.encode(
                {'user': user.to_dict(), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                '#d#JCqTTW\nilK\\7m\x0bp#\tj~#H')
            return jsonify({'token': token, 'user': user.to_dict()}), 200
        else:
            return f"user not found", 401
