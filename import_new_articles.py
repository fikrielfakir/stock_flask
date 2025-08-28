#!/usr/bin/env python3
"""
Import Script for New Article Format
Imports articles from simplified two-column format (NOM_P, Designation_P)
"""

import os
from flask_app import create_app
from flask_models import db, Supplier, Article

def determine_article_category(designation):
    """Determine article category based on designation keywords"""
    designation_lower = designation.lower()
    
    categories = {
        'Hydraulique': ['hydraulique', 'flexible', 'pompe', 'verin', 'huile', 'filtre hydraulique'],
        'Mécanique': ['roulement', 'palier', 'coussinet', 'axe', 'bague', 'courroie', 'poulie', 'mandrin'],
        'Électrique': ['cable', 'bobine', 'contacteur', 'disjoncteur', 'moteur', 'electrique', 'lampe', 'ampoule'],
        'Pneumatique': ['pneumatique', 'compresseur', 'air comprime', 'floteur'],
        'Outils': ['foret', 'cle', 'tournevis', 'pince', 'outil', 'tenaille'],
        'Consommables': ['vis', 'boulon', 'ecrou', 'joint', 'collier', 'filtre', 'bouchon'],
        'Sécurité': ['chaussure', 'securite'],
        'Divers': []
    }
    
    for category, keywords in categories.items():
        if any(keyword in designation_lower for keyword in keywords):
            return category
    
    return 'Divers'

def import_articles_from_new_format():
    """Import articles from the new simplified format"""
    articles_file = 'attached_assets/Pasted-NOM-P-Designation-P-30X860-100X640-AXE-TAMBOUR-CYLINDRIQUE-30X860-100X640-2442100-V4046-AMPOULE-ST-1756386266901_1756386266903.txt'
    
    if not os.path.exists(articles_file):
        print(f"❌ File not found: {articles_file}")
        return
    
    app = create_app()
    
    with app.app_context():
        # Get default supplier
        default_supplier = Supplier.query.first()
        default_supplier_id = default_supplier.id if default_supplier else None
        
        imported_count = 0
        skipped_count = 0
        batch_size = 100
        
        print(f"🚀 Starting import from new format file...")
        
        with open(articles_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Skip header line
        article_lines = lines[1:]
        total_lines = len(article_lines)
        
        print(f"📖 Found {total_lines} articles to process...")
        
        # Check current article count
        current_count = Article.query.count()
        print(f"📊 Current articles in database: {current_count}")
        
        for i, line in enumerate(article_lines):
            if not line.strip():
                continue
                
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            
            try:
                nom_p = parts[0].strip() if parts[0] else ''
                designation = parts[1].strip() if parts[1] else ''
                
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
                
                # Commit in batches
                if imported_count % batch_size == 0:
                    try:
                        db.session.commit()
                        print(f"✅ Batch committed: {imported_count} imported so far...")
                    except Exception as e:
                        db.session.rollback()
                        print(f"❌ Error committing batch: {e}")
                        break
                
            except Exception as e:
                print(f"❌ Error processing line {i+1}: {e}")
                continue
        
        # Final commit
        try:
            db.session.commit()
            print(f"\n🎉 Import completed!")
            print(f"✅ Articles imported: {imported_count}")
            print(f"⏭️  Articles skipped (already existed): {skipped_count}")
            
            # Final count
            final_count = Article.query.count()
            print(f"📊 Total articles now in database: {final_count}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error in final commit: {e}")

if __name__ == '__main__':
    import_articles_from_new_format()