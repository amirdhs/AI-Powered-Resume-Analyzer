import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
    # Flask App Config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    PROPAGATE_EXCEPTIONS = True

    # Database Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://resumeanalyzer_v2_user:T0xOheInOoBfysXvjLMTkI9Jode71Pae@dpg-cvrqvter433s73b278ig-a.oregon-postgres.render.com/resumeanalyzer_v2')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}

    # File Uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'pdf'}

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Swagger UI Config
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    SWAGGER_APP_NAME = 'Resume Analyzer API'