from flask import Flask, redirect, url_for
from database import close_db
from blueprints.quiz import quiz_bp
from blueprints.session import session_bp
from blueprints.notes import notes_bp


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-change-in-production'

    # Register database functions
    app.teardown_appcontext(close_db)

    # Register blueprints
    app.register_blueprint(quiz_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(notes_bp)

    # Root route - redirect to setup
    @app.route('/')
    def index():
        return redirect(url_for('quiz.setup'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
