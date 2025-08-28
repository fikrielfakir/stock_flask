from flask import Flask, jsonify, request, send_from_directory, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
from datetime import datetime
import uuid
import logging
from license_manager import license_manager

# Initialize extensions
migrate = Migrate()

def create_app():
    # Initialize Flask app
    app = Flask(__name__, static_folder='dist', static_url_path='')

    # Configuration - Local SQLite Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockceramique.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Import db from models and initialize
    from flask_models import db
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Import models and routes after db initialization
    from flask_models import Article, Supplier, Requestor, PurchaseRequest, PurchaseRequestItem, Reception, Outbound
    from routes import register_routes

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

    # License checking middleware
    def check_license():
        """Check if the application is licensed before allowing access"""
        # Skip license check for activation routes
        if request.endpoint in ['activation', 'activate_license']:
            return None
            
        if not license_manager.is_machine_licensed():
            return redirect(url_for('activation'))
        return None

    @app.before_request
    def before_request():
        license_check = check_license()
        if license_check:
            return license_check

    # Activation routes
    @app.route('/activation')
    def activation():
        machine_name = license_manager.get_machine_name()
        machine_id = license_manager.get_machine_identifier()
        return render_template('activation.html', 
                             machine_name=machine_name, 
                             machine_id=machine_id)

    @app.route('/api/activate', methods=['POST'])
    def activate_license():
        try:
            data = request.get_json()
            license_key = data.get('license_key', '').strip()
            
            if not license_key:
                return jsonify({'success': False, 'message': 'License key is required'}), 400
            
            success, message = license_manager.activate_license(license_key)
            
            if success:
                return jsonify({'success': True, 'message': message})
            else:
                return jsonify({'success': False, 'message': message}), 400
                
        except Exception as e:
            logger.error(f"Activation error: {str(e)}")
            return jsonify({'success': False, 'message': 'Activation failed due to server error'}), 500


    @app.route('/api/license-status')
    def license_status():
        try:
            info = license_manager.get_license_info()
            is_licensed = license_manager.is_machine_licensed()
            
            return jsonify({
                'success': True,
                'is_licensed': is_licensed,
                'license_info': info
            })
        except Exception as e:
            logger.error(f"License status error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to check license status'}), 500

    @app.route('/api/deactivate-license', methods=['POST'])
    def deactivate_license():
        try:
            license_manager.deactivate_license()
            return jsonify({'success': True, 'message': 'License deactivated successfully'})
        except Exception as e:
            logger.error(f"License deactivation error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to deactivate license'}), 500

    # Flask template routes
    @app.route('/')
    def dashboard():
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