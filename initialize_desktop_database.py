#!/usr/bin/env python3
"""
Initialize Desktop Database with Sample Data
Automatically populates the database when the desktop application first runs
"""

import os
import sys
from flask_app import create_app
from flask_models import db, Supplier, Article

def initialize_database_with_sample_data():
    """Initialize database with sample data for desktop deployment"""
    
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("✅ Database tables created successfully")
        
        # Check if data already exists
        if Supplier.query.count() > 0:
            print("📊 Database already contains data, skipping initialization")
            return
        
        print("🚀 Initializing database with sample data...")
        
        # Create sample suppliers
        sample_suppliers = [
            {
                'nom': 'ACME Industrial Supply',
                'contact_personne': 'Jean Dupont',
                'telephone': '+212-123-456-789',
                'email': 'contact@acme-supply.ma',
                'adresse': '123 Zone Industrielle, Casablanca'
            },
            {
                'nom': 'TechParts Morocco',
                'contact_personne': 'Sarah Martin',
                'telephone': '+212-987-654-321',
                'email': 'orders@techparts.ma',
                'adresse': '456 Avenue Hassan II, Rabat'
            },
            {
                'nom': 'MecanoDistrib',
                'contact_personne': 'Ahmed Ben Ali',
                'telephone': '+212-555-123-456',
                'email': 'sales@mecanodistrib.ma',
                'adresse': '789 Quartier Industriel, Fès'
            },
        ]
        
        supplier_objects = []
        for supplier_data in sample_suppliers:
            supplier = Supplier(**supplier_data)
            db.session.add(supplier)
            supplier_objects.append(supplier)
        
        db.session.commit()
        print(f"✅ Created {len(supplier_objects)} suppliers")
        
        # Create sample articles
        sample_articles = [
            {
                'code_article': 'AXE001',
                'designation': 'AXE TAMBOUR CYLINDRIQUE 30X860',
                'categorie': 'Mécanique',
                'marque': 'ACME',
                'reference': '30X860-100X640',
                'stock_initial': 10,
                'stock_actuel': 8,
                'unite': 'pcs',
                'prix_unitaire': 125.50,
                'seuil_minimum': 3,
                'fournisseur_id': supplier_objects[0].id
            },
            {
                'code_article': 'AMP001',
                'designation': 'AMPOULE STOP LED 24V',
                'categorie': 'Électrique',
                'marque': 'TechParts',
                'reference': '2442100-V4046',
                'stock_initial': 25,
                'stock_actuel': 18,
                'unite': 'pcs',
                'prix_unitaire': 15.75,
                'seuil_minimum': 5,
                'fournisseur_id': supplier_objects[1].id
            },
            {
                'code_article': 'HYD001',
                'designation': 'FLEXIBLE HYDRAULIQUE R2-5/8',
                'categorie': 'Hydraulique',
                'marque': 'MecanoDistrib',
                'reference': 'R2-5/8-BAGUE',
                'stock_initial': 15,
                'stock_actuel': 12,
                'unite': 'mts',
                'prix_unitaire': 89.25,
                'seuil_minimum': 4,
                'fournisseur_id': supplier_objects[2].id
            },
            {
                'code_article': 'TOOL001',
                'designation': 'CLE MIXTE EXPERT N°13',
                'categorie': 'Outils',
                'marque': 'EXPERT',
                'reference': 'EXPERT-13MM',
                'stock_initial': 8,
                'stock_actuel': 6,
                'unite': 'pcs',
                'prix_unitaire': 45.00,
                'seuil_minimum': 2,
                'fournisseur_id': supplier_objects[0].id
            },
            {
                'code_article': 'CONS001',
                'designation': 'BOULON TH 12X40',
                'categorie': 'Consommables',
                'marque': 'Standard',
                'reference': '12X40-TH',
                'stock_initial': 100,
                'stock_actuel': 75,
                'unite': 'pcs',
                'prix_unitaire': 2.50,
                'seuil_minimum': 20,
                'fournisseur_id': supplier_objects[1].id
            }
        ]
        
        for article_data in sample_articles:
            article = Article(**article_data)
            db.session.add(article)
        
        db.session.commit()
        print(f"✅ Created {len(sample_articles)} sample articles")
        
        # Summary
        suppliers_count = Supplier.query.count()
        articles_count = Article.query.count()
        print(f"\n📊 Database Initialization Complete:")
        print(f"   - Suppliers: {suppliers_count}")
        print(f"   - Articles: {articles_count}")
        print(f"✅ Desktop application is ready to use!")

if __name__ == '__main__':
    initialize_database_with_sample_data()