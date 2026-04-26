from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

def init_db(app):
    """Initialize database with application"""
    db.init_app(app)
    
    with app.app_context():
        try:
            # Test database connection
            db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful!")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # ========== NEW CODE ==========
            # Check if tickets exist, if not, add sample data
            from backend.models.ticket_model import Ticket
            ticket_count = Ticket.query.count()
            print(f"📊 Current tickets in database: {ticket_count}")
            
            if ticket_count == 0:
                print("📊 No tickets found. Adding sample data...")
                from backend.services.data_loader import DataLoader
                result = DataLoader.generate_sample_tickets(20)
                print(f"✅ {result['count']} sample tickets added successfully!")
            else:
                print(f"✅ Database already has {ticket_count} tickets")
            # ==============================
            
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            raise