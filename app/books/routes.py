from app.books.models import Book
from flask import jsonify, request, Blueprint
from google import genai
from pydantic import BaseModel
from app.core.db import db
import json

book_bp = Blueprint('books', __name__)

@book_bp.route('/', methods=['POST'])
def add_book():
    data = request.get_json()

    if not data or not 'title' in data or not 'user_id' in data:
        return jsonify({'error': 'Bad Request'}), 400
    
    book = Book(title=data['title'], user_id=data['user_id'])

    db.session.add(book)
    db.session.commit()

    return jsonify({
        'status': 'book added successfully',
        'book': {
            'id': book.id,
            'title': book.title,
            'user_id': book.user_id
        }
    }), 201


@book_bp.route('/<int:user_id>', methods=['GET'])
def list_books(user_id):
    books = Book.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'user_id': book.user_id
    } for book in books])

class Recommendation(BaseModel):
    title: str
    explanation: str

@book_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    books = Book.query.filter_by(user_id=user_id).all()
    if not books:
        return jsonify({'error': 'No books found for this user'}), 404
    if len(books) < 2:
        return jsonify({'error': 'Not enough books to provide recommendations'}), 400
    book_titles = [book.title for book in books]
    
    client = genai.Client(api_key='AIzaSyDDgXc2YV3g5MGH72V_zgNRFNJHqZ-jK00')
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