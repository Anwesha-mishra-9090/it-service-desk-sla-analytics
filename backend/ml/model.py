# Optional: ML model for SLA breach prediction
import numpy as np
from datetime import datetime, timedelta

class SLAPredictor:
    """Simple SLA breach prediction model"""
    
    def __init__(self):
        self.thresholds = {
            'High': 0.7,   # 70% confidence for breach prediction
            'Medium': 0.6,
            'Low': 0.5
        }
    
    def predict_breach_risk(self, ticket):
        """Predict risk of SLA breach"""
        risk_score = 0
        
        # Factor 1: Time remaining
        now = datetime.utcnow()
        time_remaining = (ticket.sla_deadline - now).total_seconds() / 3600
        total_allowed = {
            'High': 4,
            'Medium': 24,
            'Low': 48
        }.get(ticket.priority, 24)
        
        if time_remaining < 0:
            return 1.0  # Already breached
        
        time_factor = 1 - (time_remaining / total_allowed)
        risk_score += time_factor * 0.4  # 40% weight
        
        # Factor 2: Status
        status_weights = {
            'Open': 0.8,
            'In Progress': 0.4,
            'Resolved': 0.0,
            'Closed': 0.0
        }
        risk_score += status_weights.get(ticket.status, 0.5) * 0.3  # 30% weight
        
        # Factor 3: Historical (simplified)
        # In production, you'd use actual historical data
        risk_score += 0.3  # 30% base risk
        
        return min(risk_score, 1.0)
    
    def get_risk_level(self, risk_score):
        """Convert risk score to level"""
        if risk_score >= 0.7:
            return 'High Risk'
        elif risk_score >= 0.4:
            return 'Medium Risk'
        else:
            return 'Low Risk'