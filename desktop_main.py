#!/usr/bin/env python3
"""
StockCeramique Desktop Application
Desktop entry point for the Flask-based inventory management system using webview with splash screen
"""

import threading
import time
import webbrowser
from flask_app import create_app
from flask_models import db
import sys
import os
import socket
import logging
import requests
from tkinter import filedialog
import tkinter as tk

# Try to import webview, fallback to browser if not available
try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("⚠️  webview not available, falling back to browser mode")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get base path for PyInstaller and set up database path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_PATH = sys._MEIPASS
    # Use user's AppData directory for database
    DB_DIR = os.path.join(os.path.expanduser("~"), "StockCeramique")
    os.makedirs(DB_DIR, exist_ok=True)
    DB_PATH = os.path.join(DB_DIR, "stockceramique.db")
    # Set environment variable for Flask app to use
    os.environ['DATABASE_URL'] = f'sqlite:///{DB_PATH}'
    logger.info(f"Database will be created at: {DB_PATH}")
else:
    # Running as script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    DB_DIR = BASE_PATH
    DB_PATH = os.path.join(BASE_PATH, "stockceramique.db")

class DownloadAPI:
    """API class to handle download operations from webview"""
    
    def __init__(self, server_port):
        self.server_port = server_port
        self.downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        
    def download_file(self, url_path, suggested_filename=None):
        """Download a file from the Flask server"""
        try:
            # Create full URL
            full_url = f"http://127.0.0.1:{self.server_port}{url_path}"
            
            # Get the file from Flask server
            response = requests.get(full_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Determine filename
            if not suggested_filename:
                # Try to get filename from Content-Disposition header
                cd_header = response.headers.get('Content-Disposition', '')
                if 'filename=' in cd_header:
                    suggested_filename = cd_header.split('filename=')[1].strip('"\'')
                else:
                    suggested_filename = "download_file"
            
            # Show file save dialog
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            root.attributes('-topmost', True)  # Keep dialog on top
            
            # Get file extension from suggested filename
            file_ext = os.path.splitext(suggested_filename)[1]
            if file_ext:
                filetypes = [
                    (f"{file_ext.upper()} files", f"*{file_ext}"),
                    ("All files", "*.*")
                ]
            else:
                filetypes = [("All files", "*.*")]
            
            # Show save dialog
            file_path = filedialog.asksaveasfilename(
                title="Save file as...",
                initialfilename=suggested_filename,
                defaultextension=file_ext,
                filetypes=filetypes
            )
            
            root.destroy()
            
            if file_path:
                # Save the file
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                logger.info(f"✅ File downloaded successfully: {file_path}")
                return {"success": True, "path": file_path, "message": "File downloaded successfully!"}
            else:
                return {"success": False, "message": "Download cancelled by user"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Download request failed: {e}")
            return {"success": False, "message": f"Download failed: {str(e)}"}
        except Exception as e:
            logger.error(f"❌ Download failed: {e}")
            return {"success": False, "message": f"Download failed: {str(e)}"}

def find_free_port():
    """Find a free port from a list of common ports"""
    ports_to_try = [5001, 5002, 5003, 8001, 8002, 8003, 8080, 8081, 5000]
    
    for port in ports_to_try:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                logger.info(f"✅ Using port: {port}")
                return port
        except OSError:
            logger.debug(f"❌ Port {port} is busy")
            continue
    
    # Find any available port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        logger.info(f"✅ Using dynamic port: {port}")
        return port

def run_flask(port):
    """Run Flask server in a separate thread"""
    try:
        logger.info(f"🚀 Starting Flask server on port {port}...")
        app = create_app()
        
        # Ensure database exists and tables are created
        with app.app_context():
            db.create_all()
            logger.info("✅ Database tables created successfully")
        
        app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start Flask server: {e}")

def wait_for_server(port, timeout=30):
    """Wait for Flask server to be ready using HTTP requests"""
    start_time = time.time()
    url = f"http://127.0.0.1:{port}"
    
    logger.info("⏳ Waiting for Flask server to start...")
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                logger.info("✅ Flask server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    
    logger.error("❌ Flask server failed to start within timeout")
    return False

def safe_splash_operation(operation, *args, **kwargs):
    """Safely perform splash screen operations"""
    try:
        import pyi_splash
        if hasattr(pyi_splash, '_initialized') and not pyi_splash._initialized:
            return False
        return getattr(pyi_splash, operation)(*args, **kwargs)
    except (ImportError, RuntimeError, AttributeError) as e:
        logger.debug(f"Splash operation '{operation}' failed: {e}")
        return False

def open_browser(port):
    """Open browser after a small delay to ensure server is running"""
    time.sleep(1.5)
    webbrowser.open(f'http://127.0.0.1:{port}')

def main():
    """Main function to run the desktop application"""
    logger.info("🚀 Starting StockCeramique Desktop Application...")
    
    # Find available port
    port = find_free_port()
    
    if WEBVIEW_AVAILABLE:
        # Run with webview
        logger.info("Starting with webview interface...")
        
        # Update PyInstaller splash if available
        safe_splash_operation('update_text', 'Starting server...')
        
        # Start Flask server in background thread
        flask_thread = threading.Thread(target=run_flask, args=(port,), daemon=True)
        flask_thread.start()
        
        # Create download API instance
        download_api = DownloadAPI(port)
        
        # Wait for server to be ready
        if wait_for_server(port):
            safe_splash_operation('close')  # Close PyInstaller splash
            
            # Configure webview window
            window = webview.create_window(
                title='StockCeramique - Inventory Management',
                url=f'http://127.0.0.1:{port}',
                width=1200,
                height=800,
                min_size=(800, 600),
                resizable=True,
                shadow=True,
                js_api=download_api  # Expose download API to JavaScript
            )
            
            try:
                # Start webview (this blocks until window is closed)
                webview.start(debug=False)
            except KeyboardInterrupt:
                logger.info("Application interrupted by user")
            except Exception as e:
                logger.error(f"Webview error: {e}")
        else:
            logger.error("Failed to start server, falling back to browser")
            # Fallback to browser
            browser_thread = threading.Thread(target=open_browser, args=(port,), daemon=True)
            browser_thread.start()
            input("Press Enter to exit...")
    else:
        # Fallback to browser mode
        logger.info("Starting with browser interface...")
        
        # Create the Flask app
        app = create_app()
        
        # Ensure database exists and tables are created
        with app.app_context():
            db.create_all()
            logger.info("✅ Database tables created successfully")
        
        # Start browser in a separate thread
        browser_thread = threading.Thread(target=open_browser, args=(port,), daemon=True)
        browser_thread.start()
        
        logger.info(f"StockCeramique is running...")
        logger.info(f"Access the application at: http://127.0.0.1:{port}")
        logger.info("Close this window to exit the application")
        
        try:
            # Run the Flask application
            app.run(
                host='127.0.0.1',
                port=port,
                debug=False,
                use_reloader=False,
                threaded=True
            )
        except KeyboardInterrupt:
            logger.info("\nShutting down StockCeramique...")
        except Exception as e:
            logger.error(f"Error: {e}")
            input("Press Enter to exit...")

if __name__ == '__main__':
    main()