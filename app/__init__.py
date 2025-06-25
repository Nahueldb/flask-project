from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

from app.core.db import db, migrate


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app.core import model_registry

    from app.books import routes as books_routes
    from app.users import routes as users_routes

    app.register_blueprint(books_routes.book_bp, url_prefix='/api/books')
    app.register_blueprint(users_routes.user_bp, url_prefix='/api/users')

    return app
