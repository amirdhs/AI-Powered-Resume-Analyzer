import os
from os.path import join, dirname
from dotenv import load_dotenv

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
    # Flask App Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisissecretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:4181@localhost/resumeanalyzer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf'}

    # Flask-JWT-Extended Config (Add these!)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-jwt-key'  # Never use a default in production!
    JWT_TOKEN_LOCATION = ['headers']  # Look for JWT in the "Authorization" header
    JWT_ACCESS_TOKEN_EXPIRES = 3600   # Token expires in 1 hour (optional)