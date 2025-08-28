#!/usr/bin/env python3
"""
StockCeramique Desktop Application
Desktop entry point for the Flask-based inventory management system
"""

import os
import sys
import threading
import webbrowser
import time
from flask_app import create_app
from flask_models import db

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def open_browser():
    """Open browser after a small delay to ensure server is running"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5001')

def main():
    """Main function to run the desktop application"""
    print("Starting StockCeramique Desktop Application...")
    
    # Create the Flask app
    app = create_app()
    
    # Ensure database exists and tables are created
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("StockCeramique is running...")
    print("Access the application at: http://127.0.0.1:5001")
    print("Close this window to exit the application")
    
    try:
        # Run the Flask application
        app.run(
            host='127.0.0.1',
            port=5001,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nShutting down StockCeramique...")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()