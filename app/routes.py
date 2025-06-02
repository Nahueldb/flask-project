from app import app, db
from app.models import User, Post
from flask import jsonify, request
import requests

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data:
        return jsonify({'error': 'Bad Request'}), 400
    user_exists = User.query.filter_by(username=data['username']).first()
    if user_exists:
        return jsonify({'error': 'User already exists'}), 400
    user = User(username=data['username'], email=data['email'])

    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data:
        return jsonify({'error': 'Bad Request'}), 400
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({
        'status': 'updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
            }
        }), 200


@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()

    if not data or not 'title' in data or not 'user_id' in data:
        return jsonify({'error': 'Bad Request'}), 400
    
    book = Post(body=data['title'], user_id=data['user_id'])

    db.session.add(book)
    db.session.commit()

    return jsonify({
        'status': 'book added successfully',
        'book': {
            'id': book.id,
            'title': book.body,
            'user_id': book.user_id
        }
    }), 201


@app.route('/api/books/<int:user_id>', methods=['GET'])
def list_books(user_id):
    books = Post.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': book.id,
        'title': book.body,
        'user_id': book.user_id
    } for book in books])


@app.route('/api/books/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    books = Post.query.filter_by(user_id=user_id).all()
    if not books:
        return jsonify({'error': 'No books found for this user'}), 404
    if len(books) < 2:
        return jsonify({'error': 'Not enough books to provide recommendations'}), 400
    book_titles = [book.body for book in books]
    
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': 'AIzaSyDDgXc2YV3g5MGH72V_zgNRFNJHqZ-jK00',
    }

    json_data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': 'Recommend books based on the following titles, the answer must be in a python dict form: ' + ', '.join(book_titles),
                    },
                ],
            },
        ],
    }
    response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
        params=params,
        headers=headers,
        json=json_data,
    )


    return jsonify(response.json()), 200