from backend.utils.db import db
from datetime import datetime, timedelta
from sqlalchemy import Index

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Open', nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # SLA fields
    sla_deadline = db.Column(db.DateTime, nullable=False)
    sla_status = db.Column(db.String(20), default='Within SLA', nullable=False)
    
    # Assignment
    assigned_to = db.Column(db.String(100), nullable=True)
    
    # Metadata
    source = db.Column(db.String(50), default='manual')  # manual, csv_import, api
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_status_priority', 'status', 'priority'),
        Index('idx_sla_status', 'sla_status'),
        Index('idx_created_at', 'created_at'),
    )
    
    def __init__(self, *args, **kwargs):
        super(Ticket, self).__init__(*args, **kwargs)
        if not hasattr(self, 'sla_deadline') or not self.sla_deadline:
            self.set_sla_deadline()
    
    def set_sla_deadline(self):
        """Set SLA deadline based on priority"""
        sla_hours = {
            'High': 4,
            'Medium': 24,
            'Low': 48
        }
        hours = sla_hours.get(self.priority, 24)
        self.sla_deadline = datetime.utcnow() + timedelta(hours=hours)
    
    def update_sla_status(self):
        """Update SLA status based on current time"""
        if self.status in ['Resolved', 'Closed']:
            return
        
        now = datetime.utcnow()
        if now > self.sla_deadline:
            self.sla_status = 'Breached'
        elif (self.sla_deadline - now).total_seconds() <= 7200:  # 2 hours
            self.sla_status = 'Near Breach'
        else:
            self.sla_status = 'Within SLA'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'sla_deadline': self.sla_deadline.isoformat() if self.sla_deadline else None,
            'sla_status': self.sla_status,
            'assigned_to': self.assigned_to,
            'source': self.source
        }
    
    def __repr__(self):
        return f'<Ticket {self.id}: {self.title} - {self.status}>'