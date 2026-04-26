import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from flask_cors import CORS
from backend.config import Config
from backend.utils.db import db, init_db
from backend.routes.ticket_routes import ticket_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.upload_routes import upload_bp

# Create Flask app
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.config.from_object(Config)
CORS(app)

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(ticket_bp, url_prefix='/api/tickets')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(upload_bp, url_prefix='/api/upload')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create')
def create_page():
    return render_template('create_ticket.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

# For Gunicorn (Render)
application = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)