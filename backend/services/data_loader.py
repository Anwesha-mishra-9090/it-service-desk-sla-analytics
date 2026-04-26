import csv
from datetime import datetime, timedelta
from backend.models.ticket_model import Ticket
from backend.utils.db import db
import random

class DataLoader:
    
    @staticmethod
    def load_from_csv(file_path):
        """Load tickets from CSV file"""
        tickets_created = 0
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        # Validate required fields
                        title = row.get('title', '').strip()
                        if not title:
                            errors.append(f"Row {row_num}: Missing title")
                            continue
                        
                        priority = row.get('priority', 'Medium')
                        sla_hours = {'High': 4, 'Medium': 24, 'Low': 48}.get(priority, 24)
                        
                        ticket = Ticket(
                            title=title[:200],
                            description=row.get('description', 'No description')[:1000],
                            category=DataLoader._validate_category(row.get('category', 'Software')),
                            priority=priority,
                            status=DataLoader._validate_status(row.get('status', 'Open')),
                            assigned_to=row.get('assigned_to', None) if row.get('assigned_to') else None,
                            source='csv_import'
                        )
                        
                        db.session.add(ticket)
                        tickets_created += 1
                        
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
            
            db.session.commit()
            
            result = {'success': True, 'count': tickets_created}
            if errors:
                result['warnings'] = errors[:10]
            
            return result
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e), 'count': 0}
    
    @staticmethod
    def generate_sample_tickets(count=50):
        """Generate sample tickets for testing"""
        titles = [
            "Network connectivity issue", "Unable to access shared drive",
            "Printer not working", "Software installation failed",
            "Email sync problem", "System crash on startup",
            "VPN connection dropping", "Database connection timeout",
            "Password reset required", "Slow network performance"
        ]
        categories = ['Network', 'Software', 'Hardware']
        priorities = ['High', 'Medium', 'Low']
        statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
        
        created = 0
        for i in range(count):
            priority = random.choice(priorities)
            sla_hours = {'High': 4, 'Medium': 24, 'Low': 48}.get(priority, 24)
            
            ticket = Ticket(
                title=random.choice(titles),
                description=f"Auto-generated sample ticket #{i+1}",
                category=random.choice(categories),
                priority=priority,
                status=random.choice(statuses),
                sla_deadline=datetime.now() + timedelta(hours=sla_hours),
                sla_status='Within SLA',
                source='sample_data'
            )
            db.session.add(ticket)
            created += 1
        
        db.session.commit()
        return {'success': True, 'count': created}
    
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