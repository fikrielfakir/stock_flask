#!/usr/bin/env python3
"""
StockCeramique Flask Application
Run script for the Flask-based inventory management system
"""

from flask_app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    
    # Create database tables
    with app.app_context():
        from flask_models import db
        db.create_all()
        print("Database tables created successfully")
    
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Starting StockCeramique Flask application on port {port}")
    print("Access the application at: http://localhost:5000")
    
    # Run the Flask application
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=os.environ.get('FLASK_ENV') == 'development'
    )