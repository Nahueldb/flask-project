from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.core.db import db


class Book(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'),
                                               index=True, nullable=False)

    user: so.Mapped['User'] = so.relationship('User', back_populates='books')

    def __repr__(self):
        return '<Book {}>'.format(self.title)