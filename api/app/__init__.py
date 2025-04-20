from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
import os
import tempfile

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class='app.config.Config'):
    """Application factory function"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Set upload folder to a writable temp directory
    upload_folder = os.path.join('/tmp', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Configure Swagger UI
    swaggerui_blueprint = get_swaggerui_blueprint(
        app.config.get('SWAGGER_URL', '/api/docs'),
        app.config.get('API_URL', '/static/swagger.json'),
        config={'app_name': app.config.get('SWAGGER_APP_NAME', 'Resume Analyzer API')}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=app.config.get('SWAGGER_URL', '/api/docs'))

    # Register blueprints
    from api.app.routes import main_routes
    from api.app.auth import auth_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
