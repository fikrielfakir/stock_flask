#!/usr/bin/env python3
"""
Batch Article Import Script for StockCeramique
Imports articles in smaller batches to avoid timeout
"""

import os
from flask_app import create_app
from flask_models import db, Supplier, Article

def determine_article_category(designation):
    """Determine article category based on designation keywords"""
    designation_lower = designation.lower()
    
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

def import_articles_batch(batch_size=50):
    """Import articles in batches"""
    articles_file = 'attached_assets/Pasted-ID-P-NOM-P-Designation-P-109653-30X860-100X640-AXE-TAMBOUR-CYLINDRIQUE-30X860-100X640-159-2442100--1756385528917_1756385528918.txt'
    
    app = create_app()
    
    with app.app_context():
        # Get default supplier
        default_supplier = Supplier.query.first()
        default_supplier_id = default_supplier.id if default_supplier else None
        
        imported_count = 0
        skipped_count = 0
        
        with open(articles_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header line
        article_lines = lines[1:]
        total_lines = len(article_lines)
        
        print(f"Processing {total_lines} articles in batches of {batch_size}...")
        
        for i in range(0, total_lines, batch_size):
            batch_lines = article_lines[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            print(f"Processing batch {batch_num}/{(total_lines + batch_size - 1) // batch_size}...")
            
            for line in batch_lines:
                if not line.strip():
                    continue
                    
                parts = line.strip().split('\t')
                if len(parts) < 3:
                    continue
                
                try:
                    id_original = parts[0].strip() if parts[0] else ''
                    nom_p = parts[1].strip() if parts[1] else ''
                    designation = parts[2].strip() if parts[2] else ''
                    
                    if not designation:
                        continue
                    
                    # Create unique code_article
                    code_article = nom_p or designation[:50]
                    
                    # Check if already exists
                    existing = Article.query.filter_by(code_article=code_article).first()
                    if existing:
                        skipped_count += 1
                        continue
                    
                    # Determine category
                    category = determine_article_category(designation)
                    
                    # Create article
                    article = Article(
                        code_article=code_article,
                        designation=designation,
                        categorie=category,
                        marque='',
                        reference=nom_p,
                        stock_initial=0,
                        stock_actuel=0,
                        unite='pcs',
                        prix_unitaire=0.00,
                        seuil_minimum=5,
                        fournisseur_id=default_supplier_id
                    )
                    
                    db.session.add(article)
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Error processing line: {e}")
                    continue
            
            # Commit batch
            try:
                db.session.commit()
                print(f"✅ Batch {batch_num} committed: {imported_count} imported, {skipped_count} skipped")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error committing batch {batch_num}: {e}")
        
        print(f"\n✅ Final results: {imported_count} articles imported, {skipped_count} skipped")

if __name__ == '__main__':
    import_articles_batch(50)