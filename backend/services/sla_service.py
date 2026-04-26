from datetime import datetime
from backend.models.ticket_model import Ticket

class SLAService:
    
    @staticmethod
    def calculate_sla_metrics(tickets):
        """Calculate SLA metrics for a list of tickets"""
        total_tickets = len(tickets)
        if total_tickets == 0:
            return {
                'within_sla': 0,
                'near_breach': 0,
                'breached': 0,
                'compliance_rate': 0,
                'avg_response_time': 0
            }
        
        within = sum(1 for t in tickets if t.sla_status == 'Within SLA')
        near = sum(1 for t in tickets if t.sla_status == 'Near Breach')
        breached = sum(1 for t in tickets if t.sla_status == 'Breached')
        
        # Calculate average response time (time from creation to first update)
        response_times = []
        for ticket in tickets:
            if ticket.updated_at and ticket.created_at:
                response_time = (ticket.updated_at - ticket.created_at).total_seconds() / 3600
                if response_time > 0:
                    response_times.append(response_time)
        
        avg_response_time = round(sum(response_times) / len(response_times), 2) if response_times else 0
        
        return {
            'within_sla': within,
            'near_breach': near,
            'breached': breached,
            'compliance_rate': round((within / total_tickets) * 100, 2) if total_tickets > 0 else 0,
            'avg_response_time': avg_response_time
        }
    
    @staticmethod
    def check_breach_risk(ticket):
        """Check if a ticket is at risk of SLA breach"""
        if ticket.status in ['Resolved', 'Closed']:
            return False
        
        now = datetime.utcnow()
        time_remaining = (ticket.sla_deadline - now).total_seconds() / 3600
        
        return time_remaining <= 1  # At risk if less than 1 hour remaining
    
    @staticmethod
    def get_avg_resolution_time(tickets):
        """Calculate average resolution time in hours"""
        resolved_tickets = [t for t in tickets if t.resolved_at]
        if not resolved_tickets:
            return 0
        
        total_time = sum(
            (t.resolved_at - t.created_at).total_seconds() / 3600 
            for t in resolved_tickets
        )
        return round(total_time / len(resolved_tickets), 2)
    
    @staticmethod
    def get_sla_performance_by_priority(tickets):
        """Get SLA compliance grouped by priority"""
        priorities = ['High', 'Medium', 'Low']
        performance = {}
        
        for priority in priorities:
            priority_tickets = [t for t in tickets if t.priority == priority]
            if priority_tickets:
                within_sla = sum(1 for t in priority_tickets if t.sla_status == 'Within SLA')
                performance[priority] = {
                    'total': len(priority_tickets),
                    'compliant': within_sla,
                    'compliance_rate': round((within_sla / len(priority_tickets)) * 100, 2)
                }
            else:
                performance[priority] = {'total': 0, 'compliant': 0, 'compliance_rate': 0}
        
        return performance