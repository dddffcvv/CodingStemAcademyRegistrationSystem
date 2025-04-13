from flask import Flask
from flask_jwt_extended import JWTManager
from .routes.users import users_bp
from .routes.submissions import submissions_bp
from .routes.classes import classes_bp
from .routes.assignments import assignments_bp
from .routes.class_students import class_students_bp
from .routes.scores import scores_bp


def create_app():
    flask_app = Flask(__name__)


    flask_app.config["JWT_SECRET_KEY"] = "temporary secret key"
    jwt = JWTManager(flask_app)
    # Import and register blueprints
    flask_app.register_blueprint(users_bp)
    flask_app.register_blueprint(submissions_bp)
    flask_app.register_blueprint(classes_bp)
    flask_app.register_blueprint(assignments_bp)
    flask_app.register_blueprint(class_students_bp)
    flask_app.register_blueprint(scores_bp)

    return flask_app
