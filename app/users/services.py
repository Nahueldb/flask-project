from app.users.models import User
from app.core.db import db


class UserService:
    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        return db.session.query(User).filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)

    @staticmethod
    def create_user(username: str, email: str) -> User:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user: User, username: str | None = None, email: str | None = None) -> User:
        if username:
            user.username = username
        if email:
            user.email = email
        db.session.commit()
        return user

    @staticmethod
    def get_users() -> list[User]:
        return db.session.query(User).all()