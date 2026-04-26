import csv
import pandas as pd
from datetime import datetime, timedelta
from backend.models.ticket_model import Ticket
from backend.utils.db import db
import random

class DataLoader:
    
    @staticmethod
    def load_from_csv(file_path):
        """Load tickets from CSV file"""
        tickets_created = []
        required_columns = ['title', 'description', 'category', 'priority']
        
        try:
            df = pd.read_csv(file_path)
            
            # Validate required columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return {'success': False, 'error': f'Missing columns: {missing_columns}'}
            
            for _, row in df.iterrows():
                ticket = Ticket(
                    title=str(row.get('title', 'Incident Report'))[:200],
                    description=str(row.get('description', 'No description provided')),
                    category=DataLoader._validate_category(row.get('category', 'Software')),
                    priority=DataLoader._validate_priority(row.get('priority', 'Medium')),
                    status=DataLoader._validate_status(row.get('status', 'Open')),
                    assigned_to=str(row.get('assigned_to', 'Unassigned')) if pd.notna(row.get('assigned_to')) else None,
                    source='csv_import'
                )
                
                db.session.add(ticket)
                tickets_created.append(ticket)
            
            db.session.commit()
            return {'success': True, 'count': len(tickets_created)}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def generate_sample_tickets(count=50):
        """Generate sample tickets for testing"""
        titles = [
            "Network connectivity issue", "Unable to access shared drive",
            "Printer not working", "Software installation failed",
            "Email sync problem", "System crash on startup",
            "VPN connection dropping", "Database connection timeout",
            "Password reset required", "Slow network performance",
            "Application not responding", "File permission error",
            "Backup failed", "Security patch needed", "Hardware malfunction"
        ]
        categories = ['Network', 'Software', 'Hardware']
        priorities = ['High', 'Medium', 'Low']
        statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
        
        for i in range(count):
            priority = random.choice(priorities)
            ticket = Ticket(
                title=random.choice(titles),
                description=f"Auto-generated sample ticket #{i+1}",
                category=random.choice(categories),
                priority=priority,
                status=random.choice(statuses),
                source='sample_data'
            )
            db.session.add(ticket)
        
        db.session.commit()
        return {'success': True, 'count': count}
    
    @staticmethod
    def _validate_category(category):
        valid = ['Network', 'Software', 'Hardware']
        return category if category in valid else 'Software'
    
    @staticmethod
    def _validate_priority(priority):
        valid = ['High', 'Medium', 'Low']
        return priority if priority in valid else 'Medium'
    
    @staticmethod
    def _validate_status(status):
        valid = ['Open', 'In Progress', 'Resolved', 'Closed']
        return status if status in valid else 'Open'