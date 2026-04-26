@staticmethod
def generate_sample_tickets(count=50):
    """Generate sample tickets for testing"""
    from datetime import datetime, timedelta
    import random
    
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
        sla_hours = {'High': 4, 'Medium': 24, 'Low': 48}[priority]
        
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