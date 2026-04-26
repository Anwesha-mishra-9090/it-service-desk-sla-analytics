from flask import Blueprint, jsonify
from backend.utils.db import db
from backend.models.ticket_model import Ticket
from backend.services.analytics_service import AnalyticsService
from backend.services.sla_service import SLAService
import logging

dashboard_bp = Blueprint('dashboard', __name__)
logger = logging.getLogger(__name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """Get all dashboard statistics"""
    try:
        tickets = Ticket.query.all()
        
        # Update SLA status for all tickets
        for ticket in tickets:
            ticket.update_sla_status()
        db.session.commit()
        
        # Get analytics data with error handling
        try:
            summary = AnalyticsService.get_ticket_summary(tickets)
        except Exception as e:
            logger.error(f"Error in summary: {e}")
            summary = {
                'total_tickets': len(tickets),
                'open_tickets': 0,
                'closed_tickets': 0,
                'resolution_rate': 0,
                'high_priority_open': 0,
                'medium_priority_open': 0,
                'low_priority_open': 0
            }
        
        try:
            category_dist = AnalyticsService.get_category_distribution(tickets)
        except Exception as e:
            logger.error(f"Error in category: {e}")
            category_dist = {'Network': 0, 'Software': 0, 'Hardware': 0}
        
        try:
            priority_dist = AnalyticsService.get_priority_distribution(tickets)
        except Exception as e:
            logger.error(f"Error in priority: {e}")
            priority_dist = {'High': 0, 'Medium': 0, 'Low': 0}
        
        try:
            status_dist = AnalyticsService.get_status_distribution(tickets)
        except Exception as e:
            logger.error(f"Error in status: {e}")
            status_dist = {'Open': 0, 'In Progress': 0, 'Resolved': 0, 'Closed': 0}
        
        try:
            sla_metrics = SLAService.calculate_sla_metrics(tickets)
        except Exception as e:
            logger.error(f"Error in SLA: {e}")
            sla_metrics = {
                'within_sla': 0,
                'near_breach': 0,
                'breached': 0,
                'compliance_rate': 0,
                'avg_response_time': 0
            }
        
        try:
            trends = AnalyticsService.get_trend_data(tickets)
        except Exception as e:
            logger.error(f"Error in trends: {e}")
            trends = {}
        
        try:
            avg_resolution = SLAService.get_avg_resolution_time(tickets)
        except Exception as e:
            logger.error(f"Error in resolution: {e}")
            avg_resolution = 0
        
        try:
            sla_by_priority = SLAService.get_sla_performance_by_priority(tickets)
        except Exception as e:
            logger.error(f"Error in SLA by priority: {e}")
            sla_by_priority = {
                'High': {'total': 0, 'compliant': 0, 'compliance_rate': 0},
                'Medium': {'total': 0, 'compliant': 0, 'compliance_rate': 0},
                'Low': {'total': 0, 'compliant': 0, 'compliance_rate': 0}
            }
        
        try:
            ticket_aging = AnalyticsService.get_ticket_aging(tickets)
        except Exception as e:
            logger.error(f"Error in aging: {e}")
            ticket_aging = {'0-24h': 0, '24-48h': 0, '48h+': 0}
        
        stats = {
            'summary': summary,
            'category_distribution': category_dist,
            'priority_distribution': priority_dist,
            'status_distribution': status_dist,
            'sla_metrics': sla_metrics,
            'trends': trends,
            'avg_resolution_time': avg_resolution,
            'sla_by_priority': sla_by_priority,
            'ticket_aging': ticket_aging
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        return jsonify({'error': str(e), 'message': 'Failed to fetch dashboard statistics'}), 500