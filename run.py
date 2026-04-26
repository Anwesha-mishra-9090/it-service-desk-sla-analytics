#!/usr/bin/env python
"""Launcher for IT Service Desk"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app

if __name__ == '__main__':
    print("=" * 50)
    print("🖥️  IT Service Desk with SLA Analytics")
    print("=" * 50)
    print("Starting server...")
    print("📍 Open http://localhost:5000 in your browser")
    print("📍 Dashboard: http://localhost:5000/dashboard")
    print("📍 Create ticket: http://localhost:5000/create")
    print("Press CTRL+C to stop")
    print("=" * 50)
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)