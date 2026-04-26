import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '8f2j3k4l5m6n7p8q9r0s1t2u3v4w5x6y7z')
    
    # Get database URL from environment (Render provides this)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        # Use Render's PostgreSQL (production)
        # Fix the URL for SQLAlchemy
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Use local PostgreSQL (development)
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', 'Badal@143'))
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_NAME = os.getenv('DB_NAME', 'service_desk')
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }


