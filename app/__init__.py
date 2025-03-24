from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()


def create_app(config_class=None):  # Now accepts config_class parameter
    app = Flask(__name__)

    # Load configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        # Default configuration if none provided
        app.config.from_pyfile('config.py')

    # Initialize database
    db.init_app(app)

    # Swagger configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Resume Analyzer API"}
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Register blueprints
    from app.routes import main_routes
    from app.auth import auth_routes

    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    return app