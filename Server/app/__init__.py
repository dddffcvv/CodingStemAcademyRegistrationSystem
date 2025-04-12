from flask import Flask

def create_app():
    flask_app = Flask(__name__)

    # Import and register blueprints
    from .routes import app
    flask_app.register_blueprint(app)

    return flask_app
