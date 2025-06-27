from flask import jsonify, current_app
from pydantic import ValidationError


class UserNotFoundError(Exception):
    """Custom exception for user not found errors."""
    def __init__(self):
        super().__init__("User/s not found.")


class UserAlreadyExistsError(Exception):
    """Custom exception for user already exists errors."""
    def __init__(self, username=None):
        super().__init__(f"User '{username}' already exists." if username else "User already exists.")


class BookNotFoundError(Exception):
    """Custom exception for book not found errors."""
    def __init__(self):
        super().__init__("Book not found.")


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        current_app.logger.error(f"404 error: {error}")
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        current_app.logger.error(f"500 error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(400)
    def bad_request_error(error):
        current_app.logger.error(f"400 error: {error}")
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(UserNotFoundError)
    def handle_user_not_found(error):
        current_app.logger.error(error)
        return jsonify({"error": "User/s not found"}), 404

    @app.errorhandler(UserAlreadyExistsError)
    def handle_user_already_exists(error):
        current_app.logger.error(error)
        return jsonify({"error": "User already exists"}), 409

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        current_app.logger.error(f"Validation error: {error}")
        return jsonify({"error": "Validation error", "details": str(error)}), 422