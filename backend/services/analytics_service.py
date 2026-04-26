from datetime import datetime, timedelta
from collections import Counter
from backend.models.ticket_model import Ticket

class AnalyticsService:
    
    @staticmethod
    def get_ticket_summary(tickets):
        """Get summary statistics for tickets"""
        total = len(tickets)
        open_tickets = sum(1 for t in tickets if t.status in ['Open', 'In Progress'])
        closed_tickets = sum(1 for t in tickets if t.status in ['Resolved', 'Closed'])
        
        # Calculate by priority
        high_priority_open = sum(1 for t in tickets if t.priority == 'High' and t.status in ['Open', 'In Progress'])
        medium_priority_open = sum(1 for t in tickets if t.priority == 'Medium' and t.status in ['Open', 'In Progress'])
        low_priority_open = sum(1 for t in tickets if t.priority == 'Low' and t.status in ['Open', 'In Progress'])
        
        return {
            'total_tickets': total,
            'open_tickets': open_tickets,
            'closed_tickets': closed_tickets,
            'resolution_rate': round((closed_tickets / total) * 100, 2) if total > 0 else 0,
            'high_priority_open': high_priority_open,
            'medium_priority_open': medium_priority_open,
            'low_priority_open': low_priority_open
        }
    
    @staticmethod
    def get_category_distribution(tickets):
        """Get ticket distribution by category"""
        categories = {}
        for category in ['Network', 'Software', 'Hardware']:
            categories[category] = sum(1 for t in tickets if t.category == category)
        return categories
    
    @staticmethod
    def get_priority_distribution(tickets):
        """Get ticket distribution by priority"""
        priorities = {}
        for priority in ['High', 'Medium', 'Low']:
            priorities[priority] = sum(1 for t in tickets if t.priority == priority)
        return priorities
    
    @staticmethod
    def get_trend_data(tickets, days=7):
        """Get ticket creation trends for last N days"""
        trends = {}
        today = datetime.utcnow().date()
        
        for i in range(days):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            trends[date_str] = sum(
                1 for t in tickets 
                if t.created_at.date() == date
            )
        
        return dict(sorted(trends.items()))
    
    @staticmethod
    def get_status_distribution(tickets):
        """Get ticket distribution by status"""
        statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
        return {
            status: sum(1 for t in tickets if t.status == status)
            for status in statuses
        }
    
    @staticmethod
    def get_ticket_aging(tickets):
        """Calculate aging of open tickets"""
        now = datetime.utcnow()
        aging = {
            '0-24h': 0,
            '24-48h': 0,
            '48h+': 0
        }
        
        open_tickets = [t for t in tickets if t.status in ['Open', 'In Progress']]
        for ticket in open_tickets:
            age = (now - ticket.created_at).total_seconds() / 3600
            if age <= 24:
                aging['0-24h'] += 1
            elif age <= 48:
                aging['24-48h'] += 1
            else:
                aging['48h+'] += 1
        
        return aging