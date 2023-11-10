from flaskapp.user_management.models import User
from sqlalchemy import select


def get_user_by_id(user_id: int) -> User:
    return User.query.get(user_id)


def get_user_by_email(email: str) -> User:
    return User.query.filter(User.email == email).first()