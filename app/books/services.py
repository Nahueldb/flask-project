import os
from app.books.models import Book
from app.books.schemas import Recommendation
from app.core.db import db
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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


def get_gemini_client():
    """Get a Gemini client instance."""
    return genai.Client(api_key=GEMINI_API_KEY)

class RecommendationService:
    @staticmethod
    def get_recommendations(user_id: int, book_titles: list[str]) -> list[dict]:
        """Get book recommendations for a user."""
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents="Generate a list of book recommendations based on the following titles (the explanation must be in spanish): " + ", ".join(book_titles),
            config={
                "response_mime_type": "application/json",
                "response_schema": list[Recommendation],
            },
        )

        return response