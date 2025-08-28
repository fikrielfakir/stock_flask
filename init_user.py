#!/usr/bin/env python3
"""
Initialize the default user for Orbit system
Creates user: mustapha with password: 26cedesa8@2024
"""

from flask_app import create_app
from flask_models import db, User

def init_default_user():
    app = create_app()
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username='mustapha').first()
        
        if existing_user:
            print("User 'mustapha' already exists")
            return
        
        # Create the default user
        user = User(
            username='mustapha',
            full_name='Mustapha',
            email='mustapha@orbit.com',
            is_active=True
        )
        user.set_password('26cedesa8@2024')
        
        db.session.add(user)
        db.session.commit()
        
        print("Default user 'mustapha' created successfully")
        print("Username: mustapha")
        print("Password: 26cedesa8@2024")

if __name__ == '__main__':
    init_default_user()