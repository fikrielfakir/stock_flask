    #!/usr/bin/env python3
    """
    StockCeramique Desktop Application
    Desktop entry point for the Flask-based inventory management system using webview with splash screen
    """

    import threading
    import time
    import webview
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

        def show_downloads_folder(self):
            """Open the downloads folder in file explorer"""
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(self.downloads_dir)
                elif os.name == 'posix':  # macOS/Linux
                    os.system(f'open "{self.downloads_dir}"' if sys.platform == 'darwin' else f'xdg-open "{self.downloads_dir}"')
                return {"success": True, "message": "Downloads folder opened"}
            except Exception as e:
                logger.error(f"❌ Failed to open downloads folder: {e}")
                return {"success": False, "message": f"Failed to open downloads folder: {str(e)}"}

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

    def create_splash_screen():
        """Create splash screen HTML content"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>StockCeramique Loading</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    color: white;
                    overflow: hidden;
                }
                .splash-container {
                    text-align: center;
                    animation: fadeIn 0.8s ease-in;
                }
                .logo {
                    font-size: 3rem;
                    font-weight: bold;
                    margin-bottom: 1rem;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .subtitle {
                    font-size: 1.2rem;
                    opacity: 0.9;
                    margin-bottom: 2rem;
                }
                .spinner {
                    width: 40px;
                    height: 40px;
                    margin: 0 auto;
                    border: 4px solid rgba(255,255,255,0.3);
                    border-top: 4px solid white;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
                .status {
                    margin-top: 1rem;
                    font-size: 0.9rem;
                    opacity: 0.8;
                    min-height: 20px;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(-20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>
        </head>
        <body>
            <div class="splash-container">
                <div class="logo">StockCeramique</div>
                <div class="subtitle">Inventory Management System</div>
                <div class="spinner"></div>
                <div class="status" id="status">Starting server...</div>
            </div>
            <script>
                // Update status messages
                const statusEl = document.getElementById('status');
                const messages = [
                    'Initializing application...',
                    'Setting up database...',
                    'Starting Flask server...',
                    'Loading interface...'
                ];
                let messageIndex = 0;

                setInterval(() => {
                    if (messageIndex < messages.length - 1) {
                        messageIndex++;
                        statusEl.textContent = messages[messageIndex];
                    }
                }, 1000);
            </script>
        </body>
        </html>
        """

    def switch_to_main_app(port):
        """Switch from splash screen to main application"""
        url = f"http://127.0.0.1:{port}"

        if wait_for_server(port):
            logger.info("🔄 Switching to main application...")
            # Update the webview URL to the main application
            if webview.windows:
                webview.windows[0].load_url(url)
            return True
        else:
            logger.error("❌ Server failed to start within timeout period")
            # Show error in the webview
            error_html = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        text-align: center;
                        padding: 50px;
                        background: #f5f5f5;
                        color: #333;
                    }}
                    .error-container {{
                        max-width: 500px;
                        margin: 0 auto;
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    h2 {{ color: #e74c3c; margin-bottom: 20px; }}
                    p {{ line-height: 1.6; margin-bottom: 20px; }}
                    .retry-btn {{
                        background: #3498db;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                    }}
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h2>⚠️ Server Startup Error</h2>
                    <p>The Flask server failed to start properly.</p>
                    <p>Please close the application and try again.</p>
                    <p>If the problem persists, check if port {port} is available.</p>
                </div>
            </body>
            </html>
            """
            if webview.windows:
                webview.windows[0].load_html(error_html)
            return False

    def safe_input_wait(message="Press any key to exit..."):
        """Safely wait for user input, with fallbacks for different environments"""
        logger.info(message)

        # Check if we have stdin available
        if hasattr(sys.stdin, 'read') and sys.stdin.isatty():
            try:
                input(message)
                return
            except (EOFError, RuntimeError):
                pass

        # Fallback 1: Try using a simple time delay
        logger.info("Console input not available. Waiting 5 seconds before exit...")
        time.sleep(5)

    def open_with_webview_direct(url, port):
        """Open webview directly to the main application (no splash screen)"""
        try:
            logger.info("🖥️ Opening webview with main application...")

            # Create download API instance
            download_api = DownloadAPI(port)

            # Create webview window directly with the main app URL
            webview.create_window(
                "StockCeramique - Inventory Management",
                url,
                width=1200,
                height=800,
                min_size=(800, 600),
                resizable=True,
                maximized=False,
                js_api=download_api  # Expose download API to JavaScript
            )

            # Start webview (this blocks until window is closed)
            webview.start(debug=False)
            return True

        except Exception as e:
            logger.error(f"❌ Webview failed: {e}")
            return False

    def open_with_webview_splash(url, port):
        """Try to open with webview and automatic splash screen (fallback option)"""
        try:
            logger.info("🖥️ Attempting to open with webview and splash...")

            # Create download API instance
            download_api = DownloadAPI(port)

            # Create webview window with splash screen
            webview.create_window(
                "StockCeramique - Inventory Management",
                html=create_splash_screen(),  # Start with splash screen
                width=1200,
                height=800,
                min_size=(800, 600),
                resizable=True,
                maximized=False,
                js_api=download_api  # Expose download API to JavaScript
            )

            # Start server switching in background
            switch_thread = threading.Thread(target=switch_to_main_app, args=(port,), daemon=True)
            switch_thread.start()

            # Start webview (this blocks until window is closed)
            webview.start(debug=False)
            return True

        except Exception as e:
            logger.error(f"❌ Webview failed: {e}")
            return False

    def open_with_browser(url):
        """Open with default browser"""
        try:
            logger.info("🌐 Opening with default browser...")
            webbrowser.open(url)
            logger.info("✅ Browser opened successfully!")
            logger.info("📋 Keep this console window open to keep the server running")
            logger.info("📋 Close this window or press Ctrl+C to stop the server")
            return True
        except Exception as e:
            logger.error(f"❌ Browser failed: {e}")
            return False

    def keep_alive():
        """Keep the application running when using browser"""
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("👋 Application stopped by user")

    def main():
        """Main function to run the desktop application"""
        try:
            logger.info("🚀 Starting StockCeramique Desktop Application...")

            # Update PyInstaller splash screen
            safe_splash_operation('update_text', 'Initializing application...')

            # Find available port
            port = find_free_port()

            # Update splash
            safe_splash_operation('update_text', 'Starting Flask server...')

            # Start Flask server
            flask_thread = threading.Thread(target=run_flask, args=(port,), daemon=True)
            flask_thread.start()

            # Update splash
            safe_splash_operation('update_text', 'Waiting for server...')

            # Wait for server to be ready before showing webview
            if wait_for_server(port):
                logger.info("✅ Server is ready!")

                # Update splash one more time
                safe_splash_operation('update_text', 'Loading interface...')
                time.sleep(0.5)  # Brief pause to show the message

                # Close PyInstaller splash screen
                safe_splash_operation('close')

                # Server URL
                url = f"http://127.0.0.1:{port}"
                logger.info(f"🌐 Server ready at: {url}")

                # Try webview first, fallback to browser
                if not open_with_webview_direct(url, port):
                    logger.info("🔄 Webview failed, trying browser fallback...")

                    if open_with_browser(url):
                        # Keep server running for browser
                        keep_alive()
                    else:
                        logger.error("❌ Both webview and browser failed!")
                        logger.info(f"📋 Try manually opening: {url}")
                        safe_input_wait("Both webview and browser failed. Press any key to exit...")
            else:
                logger.error("❌ Flask server failed to start")
                safe_splash_operation('close')
                safe_input_wait("Flask server failed to start. Press any key to exit...")

        except Exception as e:
            logger.error(f"❌ Application failed to start: {e}")
            import traceback
            logger.error(traceback.format_exc())

            # Try to close splash screen
            safe_splash_operation('close')

            safe_input_wait("Application failed to start. Press any key to exit...")
            sys.exit(1)

    if __name__ == '__main__':
        main()