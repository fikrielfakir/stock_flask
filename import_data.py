#!/usr/bin/env python3
"""
Data Import Script for StockCeramique
Imports suppliers and articles from tab-separated text files
"""

import re
import os
from flask_app import create_app
from flask_models import db, Supplier, Article
from datetime import datetime

def clean_phone_number(phone):
    """Clean and normalize phone numbers"""
    if not phone or phone in ['00', '000', '0000000000', '00000000000', '000000000']:
        return None
    # Remove common invalid patterns
    phone = str(phone).strip()
    if phone.startswith('0') and len(phone) > 1:
        return phone
    return phone if phone != '0' else None

def clean_email(email):
    """Clean and validate email addresses"""
    if not email or email.strip() == '':
        return None
    email = email.strip()
    # Basic email validation
    if '@' in email and '.' in email:
        return email
    return None

def clean_text(text):
    """Clean text fields"""
    if not text or str(text).strip() == '':
        return None
    return str(text).strip()

def parse_suppliers_file(file_path):
    """Parse the suppliers tab-separated file"""
    suppliers = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header line
    for line in lines[1:]:
        if not line.strip():
            continue
            
        # Split by tabs
        parts = line.strip().split('\t')
        if len(parts) < 8:
            continue
            
        try:
            supplier_data = {
                'id_original': clean_text(parts[0]),
                'nom': clean_text(parts[1]),
                'adresse': clean_text(parts[2]),
                'telephone': clean_phone_number(parts[3]),
                'fax': clean_phone_number(parts[4]),
                'email': clean_email(parts[5]),
                'id_d': clean_text(parts[6]),
                'remarque': clean_text(parts[7]) if len(parts) > 7 else None
            }
            
            if supplier_data['nom']:  # Only add if name exists
                suppliers.append(supplier_data)
                
        except Exception as e:
            print(f"Error parsing supplier line: {line.strip()[:100]}... - {e}")
            continue
    
    return suppliers

def parse_articles_file(file_path):
    """Parse the articles tab-separated file"""
    articles = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header line
    for line in lines[1:]:
        if not line.strip():
            continue
            
        # Split by tabs
        parts = line.strip().split('\t')
        if len(parts) < 3:
            continue
            
        try:
            article_data = {
                'id_original': clean_text(parts[0]),
                'nom_p': clean_text(parts[1]),
                'designation': clean_text(parts[2])
            }
            
            if article_data['designation']:  # Only add if designation exists
                articles.append(article_data)
                
        except Exception as e:
            print(f"Error parsing article line: {line.strip()[:100]}... - {e}")
            continue
    
    return articles

def determine_article_category(designation):
    """Determine article category based on designation keywords"""
    designation_lower = designation.lower()
    
    # Category mapping based on keywords
    categories = {
        'Hydraulique': ['hydraulique', 'flexible', 'pompe', 'verin', 'huile', 'filtre hydraulique'],
        'Mécanique': ['roulement', 'palier', 'coussinet', 'axe', 'bague', 'courroie', 'poulie'],
        'Électrique': ['cable', 'bobine', 'contacteur', 'disjoncteur', 'moteur', 'electrique', 'lampe'],
        'Pneumatique': ['pneumatique', 'compresseur', 'air comprime', 'floteur'],
        'Outils': ['foret', 'cle', 'tournevis', 'pince', 'outil'],
        'Consommables': ['vis', 'boulon', 'ecrou', 'joint', 'collier', 'filtre'],
        'Divers': []
    }
    
    for category, keywords in categories.items():
        if any(keyword in designation_lower for keyword in keywords):
            return category
    
    return 'Divers'

def import_suppliers(suppliers_data):
    """Import suppliers into the database"""
    imported_count = 0
    skipped_count = 0
    
    print(f"Importing {len(suppliers_data)} suppliers...")
    
    for supplier_data in suppliers_data:
        try:
            # Check if supplier already exists
            existing = Supplier.query.filter_by(nom=supplier_data['nom']).first()
            if existing:
                print(f"Supplier already exists: {supplier_data['nom']}")
                skipped_count += 1
                continue
            
            # Create new supplier
            supplier = Supplier(
                nom=supplier_data['nom'],
                adresse=supplier_data['adresse'],
                telephone=supplier_data['telephone'],
                email=supplier_data['email'],
                contact=supplier_data['remarque'],  # Use remarque as contact info
                conditions_paiement='Net 30',  # Default payment terms
                delai_livraison=7  # Default delivery time
            )
            
            db.session.add(supplier)
            imported_count += 1
            
            if imported_count % 50 == 0:
                print(f"Imported {imported_count} suppliers...")
                
        except Exception as e:
            print(f"Error importing supplier {supplier_data['nom']}: {e}")
            continue
    
    try:
        db.session.commit()
        print(f"✅ Successfully imported {imported_count} suppliers, skipped {skipped_count}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error committing suppliers: {e}")
        return 0
    
    return imported_count

def import_articles(articles_data):
    """Import articles into the database"""
    imported_count = 0
    skipped_count = 0
    
    print(f"Importing {len(articles_data)} articles...")
    
    # Get first supplier as default (you can modify this logic)
    default_supplier = Supplier.query.first()
    default_supplier_id = default_supplier.id if default_supplier else None
    
    for article_data in articles_data:
        try:
            # Create code_article from nom_p or use designation
            code_article = article_data['nom_p'] or article_data['designation'][:50]
            
            # Check if article already exists
            existing = Article.query.filter_by(code_article=code_article).first()
            if existing:
                print(f"Article already exists: {code_article}")
                skipped_count += 1
                continue
            
            # Determine category
            category = determine_article_category(article_data['designation'])
            
            # Create new article
            article = Article(
                code_article=code_article,
                designation=article_data['designation'],
                categorie=category,
                marque='',  # Empty for now
                reference=article_data['nom_p'],
                stock_initial=0,
                stock_actuel=0,
                unite='pcs',
                prix_unitaire=0.00,
                seuil_minimum=5,
                fournisseur_id=default_supplier_id
            )
            
            db.session.add(article)
            imported_count += 1
            
            if imported_count % 100 == 0:
                print(f"Imported {imported_count} articles...")
                
        except Exception as e:
            print(f"Error importing article {article_data.get('designation', 'Unknown')}: {e}")
            continue
    
    try:
        db.session.commit()
        print(f"✅ Successfully imported {imported_count} articles, skipped {skipped_count}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error committing articles: {e}")
        return 0
    
    return imported_count

def main():
    """Main import function"""
    print("🚀 Starting data import for StockCeramique...")
    
    # File paths
    suppliers_file = 'attached_assets/Pasted-ID-F-NOM-F-ADRESSE-F-TEL-F-FAX-F-EMAIL-F-ID-D-REMARQUE-F-384-A-D-S-INDUSTRIE-MAROC-0539714269-1--1756385420545_1756385420546.txt'
    articles_file = 'attached_assets/Pasted-ID-P-NOM-P-Designation-P-109653-30X860-100X640-AXE-TAMBOUR-CYLINDRIQUE-30X860-100X640-159-2442100--1756385528917_1756385528918.txt'
    
    # Check if files exist
    if not os.path.exists(suppliers_file):
        print(f"❌ Suppliers file not found: {suppliers_file}")
        return
    
    if not os.path.exists(articles_file):
        print(f"❌ Articles file not found: {articles_file}")
        return
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        try:
            # Parse data files
            print("📖 Parsing suppliers file...")
            suppliers_data = parse_suppliers_file(suppliers_file)
            print(f"Found {len(suppliers_data)} suppliers to import")
            
            print("📖 Parsing articles file...")
            articles_data = parse_articles_file(articles_file)
            print(f"Found {len(articles_data)} articles to import")
            
            # Import suppliers first
            print("\n" + "="*50)
            print("IMPORTING SUPPLIERS")
            print("="*50)
            suppliers_imported = import_suppliers(suppliers_data)
            
            # Import articles
            print("\n" + "="*50)
            print("IMPORTING ARTICLES")
            print("="*50)
            articles_imported = import_articles(articles_data)
            
            print("\n" + "="*50)
            print("IMPORT SUMMARY")
            print("="*50)
            print(f"✅ Suppliers imported: {suppliers_imported}")
            print(f"✅ Articles imported: {articles_imported}")
            print("✅ Data import completed successfully!")
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()