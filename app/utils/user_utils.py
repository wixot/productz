from flask import current_app
from flask_login import current_user

from app.schemas import User


def get_request_user(api_key):
    if api_key:
        flask_app = current_app._get_current_object()
        user = User.objects.filter(api_key=api_key).first()
    else:
        user = User.objects(id=current_user.id).first()

    return user