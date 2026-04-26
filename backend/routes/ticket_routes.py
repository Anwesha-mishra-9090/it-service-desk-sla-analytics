from flask import Blueprint, request, jsonify
from backend.utils.db import db
from backend.models.ticket_model import Ticket
from backend.services.sla_service import SLAService
from datetime import datetime
import logging

ticket_bp = Blueprint('tickets', __name__)
logger = logging.getLogger(__name__)

@ticket_bp.route('/', methods=['GET'])
def get_tickets():
    """Get all tickets with optional filters"""
    try:
        status = request.args.get('status')
        priority = request.args.get('priority')
        category = request.args.get('category')
        
        query = Ticket.query
        
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if category:
            query = query.filter_by(category=category)
        
        tickets = query.order_by(Ticket.created_at.desc()).all()
        return jsonify([t.to_dict() for t in tickets])
    except Exception as e:
        logger.error(f"Error fetching tickets: {str(e)}")
        return jsonify({'error': 'Failed to fetch tickets'}), 500

@ticket_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get single ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        return jsonify(ticket.to_dict())
    except Exception as e:
        logger.error(f"Error fetching ticket {ticket_id}: {str(e)}")
        return jsonify({'error': 'Ticket not found'}), 404

@ticket_bp.route('/', methods=['POST'])
def create_ticket():
    """Create new ticket"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'priority']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        ticket = Ticket(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            priority=data['priority'],
            assigned_to=data.get('assigned_to'),
            source='manual'
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        logger.info(f"Ticket created: {ticket.id}")
        return jsonify(ticket.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating ticket: {str(e)}")
        return jsonify({'error': 'Failed to create ticket'}), 500

@ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """Update ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.json
        
        if 'status' in data:
            ticket.status = data['status']
            if data['status'] in ['Resolved', 'Closed'] and not ticket.resolved_at:
                ticket.resolved_at = datetime.utcnow()
        
        if 'assigned_to' in data:
            ticket.assigned_to = data['assigned_to']
        
        if 'priority' in data:
            ticket.priority = data['priority']
            ticket.set_sla_deadline()  # Reset SLA deadline when priority changes
        
        ticket.update_sla_status()
        db.session.commit()
        
        logger.info(f"Ticket updated: {ticket_id}")
        return jsonify(ticket.to_dict())
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating ticket {ticket_id}: {str(e)}")
        return jsonify({'error': 'Failed to update ticket'}), 500

@ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    """Delete ticket"""
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()
        
        logger.info(f"Ticket deleted: {ticket_id}")
        return jsonify({'message': 'Ticket deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting ticket {ticket_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete ticket'}), 500

@ticket_bp.route('/sla/check', methods=['GET'])
def check_sla_status():
    """Check SLA status for all tickets"""
    try:
        tickets = Ticket.query.all()
        at_risk = []
        
        for ticket in tickets:
            ticket.update_sla_status()
            if SLAService.check_breach_risk(ticket):
                at_risk.append(ticket.to_dict())
        
        db.session.commit()
        return jsonify({
            'at_risk_tickets': at_risk,
            'count': len(at_risk)
        })
        
    except Exception as e:
        logger.error(f"Error checking SLA: {str(e)}")
        return jsonify({'error': 'Failed to check SLA status'}), 500