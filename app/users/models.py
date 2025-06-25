from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.core.db import db

class User(db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True, nullable=False)

    books: so.WriteOnlyMapped['Book'] = so.relationship('Book', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return '<User {}>'.format(self.username)
