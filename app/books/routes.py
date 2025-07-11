from flask import jsonify, request, Blueprint
from google import genai
from app.books.schemas import Recommendation, BookCreateSchema, BookSchema
from app.books.services import BookService
from app.users.services import UserService
from app.core.error_handlers import UserNotFoundError, BookNotFoundError
import json
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
book_bp = Blueprint('books', __name__)

@book_bp.route('/', methods=['POST'])
def add_book():
    data = BookCreateSchema(**request.get_json())

    user_exists = UserService.get_user_by_id(data.user_id)
    if not user_exists:
        raise UserNotFoundError()

    book = BookService.add_book(
        title=data.title,
        user_id=data.user_id
    )

    return jsonify({
        'status': 'book added successfully',
        'book': BookSchema.model_validate(book).model_dump()
    }), 201


@book_bp.route('/<int:user_id>', methods=['GET'])
def list_books(user_id):
    books = BookService.get_books_by_user_id(user_id)
    user_exists = UserService.get_user_by_id(user_id)
    if not user_exists:
        raise UserNotFoundError()
    if not books:
        raise BookNotFoundError()
    return jsonify([
        BookSchema.model_validate(book).model_dump()
        for book in books
    ]), 200


@book_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    books = BookService.get_books_by_user_id(user_id)
    if not books:
        return jsonify({'error': 'No books found for this user'}), 404
    if len(books) < 2:
        return jsonify({'error': 'Not enough books to provide recommendations'}), 400
    book_titles = [book.title for book in books]

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Generate a list of book recommendations based on the following titles (the explanation must be in spanish): " + ", ".join(book_titles),
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Recommendation],
        },
    )

    _response_json = json.loads(response.text)

    return jsonify(_response_json), 200