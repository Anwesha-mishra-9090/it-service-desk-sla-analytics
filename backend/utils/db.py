from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database with application"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        try:
            # Test database connection
            db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful!")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
        except SQLAlchemyError as e:
            print(f"❌ Database connection failed: {str(e)}")
            print("\nPlease check:")
            print("1. PostgreSQL service is running")
            print("2. Database credentials in .env file are correct")
            print("3. Database 'service_desk' exists")
            raise

def test_connection(app):
    """Test database connection"""
    with app.app_context():
        try:
            result = db.session.execute(text('SELECT version()')).fetchone()
            print(f"✅ Connected to: {result[0]}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False