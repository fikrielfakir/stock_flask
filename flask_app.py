from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
from datetime import datetime
import uuid
import logging

# Initialize extensions
migrate = Migrate()

def create_app():
    # Initialize Flask app
    app = Flask(__name__, static_folder='dist', static_url_path='')

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/stockceramique')
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