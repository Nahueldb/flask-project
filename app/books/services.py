from app.books.models import Book
from app.core.db import db


class BookService:
    @staticmethod
    def get_books_by_user_id(user_id: int) -> list[Book]:
        """Retrieve all books for a given user by user ID."""
        return db.session.query(Book).filter_by(user_id=user_id).all()

    @staticmethod
    def add_book(title: str, user_id: int) -> Book:
        book = Book(title=title, user_id=user_id)
        db.session.add(book)
        db.session.commit()
        return book
