from app import app, db
from app.models import User
from flask import jsonify, request

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