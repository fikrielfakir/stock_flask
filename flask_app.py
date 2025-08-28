from flask import Flask, jsonify, request, send_from_directory, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
from datetime import datetime
import uuid
import logging
# License managers removed for Replit environment

# Initialize extensions
migrate = Migrate()

def create_app():
    # Initialize Flask app
    app = Flask(__name__, static_folder='dist', static_url_path='')

    # Configuration - PostgreSQL Database
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'connect_timeout': 10,
            'sslmode': 'prefer'
        }
    }
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

    # Import db from models and initialize
    from flask_models import db
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Import models and routes after db initialization
    from flask_models import Article, Supplier, Requestor, PurchaseRequest, PurchaseRequestItem, Reception, Outbound, User, UserSession
    from routes import register_routes
    from functools import wraps
    
    # Authentication middleware
    def require_auth(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return redirect('/login')
            
            token = auth_header.split(' ')[1]
            session = UserSession.query.filter_by(session_token=token).first()
            
            if not session or not session.is_valid():
                return redirect('/login')
            
            # Update last activity
            session.user.last_login = datetime.utcnow()
            db.session.commit()
            
            return f(*args, **kwargs)
        return decorated_function

    # Register all routes
    register_routes(app, db)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500

    # License checking removed for Replit environment

    # License and activation routes removed for Replit environment

    # Login route
    @app.route('/login')
    def login_page():
        return render_template('login.html')
    
    # Flask template routes
    @app.route('/')
    def dashboard():
        # Check for session in cookies or localStorage (handled by frontend)
        return render_template('dashboard.html')
    
    @app.route('/articles')
    def articles():
        return render_template('articles.html')
    
    @app.route('/suppliers')
    def suppliers():
        return render_template('suppliers.html')
    
    @app.route('/requestors')
    def requestors():
        return render_template('requestors.html')
    
    @app.route('/purchase-requests')
    def purchase_requests():
        return render_template('purchase_requests.html')
    
    @app.route('/reception')
    def reception():
        return render_template('reception.html')
    
    @app.route('/outbound')
    def outbound():
        return render_template('outbound.html')
    
    @app.route('/analytics')
    def analytics():
        return render_template('analytics.html')
    
    @app.route('/purchase-follow')
    def purchase_follow():
        return render_template('purchase_follow.html')
    
    @app.route('/stock-status')
    def stock_status():
        return render_template('stock_status.html')
    
    @app.route('/reports')
    def reports():
        return render_template('reports.html')
    
    @app.route('/notifications')
    def notifications():
        return render_template('notifications.html')
    
    @app.route('/profile')
    def profile():
        return render_template('profile.html')
    
    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Create tables if they don't exist
    with app.app_context():
        from flask_models import db
        db.create_all()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')