#!/usr/bin/env python3
"""
Article Data Import Script for StockCéramique
Imports articles from the provided CSV data file
"""

import csv
import os
import sys
from flask_app import create_app
from flask_models import db, Article
from decimal import Decimal
import uuid

def generate_code_article(designation, reference):
    """Generate a unique article code based on designation and reference"""
    # Use reference if available, otherwise generate from designation
    if reference and reference.strip() and reference.strip() != designation.strip():
        return reference.strip()[:50]  # Limit to 50 chars
    else:
        # Generate code from first words of designation
        words = designation.strip().split()[:3]  # First 3 words
        code = ''.join(word[:4].upper() for word in words if word)
        return code[:20] if code else str(uuid.uuid4())[:8].upper()

def determine_category(designation):
    """Determine category based on designation keywords"""
    designation_lower = designation.lower()
    
    if any(word in designation_lower for word in ['moteur', 'motor', 'electrique']):
        return 'MOTEURS'
    elif any(word in designation_lower for word in ['huile', 'oil', 'lubrifiant']):
        return 'LUBRIFIANTS'
    elif any(word in designation_lower for word in ['courroie', 'belt']):
        return 'COURROIES'
    elif any(word in designation_lower for word in ['tube', 'tuyau', 'pipe']):
        return 'TUYAUTERIE'
    elif any(word in designation_lower for word in ['vis', 'boulon', 'ecrou', 'screw']):
        return 'VISSERIE'
    elif any(word in designation_lower for word in ['cable', 'fil', 'electrique']):
        return 'ELECTRICITE'
    elif any(word in designation_lower for word in ['gant', 'protection', 'securite']):
        return 'PROTECTION'
    elif any(word in designation_lower for word in ['peinture', 'diluant', 'paint']):
        return 'PEINTURE'
    elif any(word in designation_lower for word in ['roulement', 'bearing']):
        return 'ROULEMENTS'
    elif any(word in designation_lower for word in ['pompe', 'pump']):
        return 'POMPES'
    elif any(word in designation_lower for word in ['valve', 'vanne', 'robinet']):
        return 'VANNES'
    elif any(word in designation_lower for word in ['contacteur', 'disjoncteur', 'electrique']):
        return 'ELECTRICITE'
    elif any(word in designation_lower for word in ['cle', 'outil', 'tool']):
        return 'OUTILS'
    elif any(word in designation_lower for word in ['tole', 'fer', 'metal']):
        return 'METALLURGIE'
    else:
        return 'DIVERS'

def import_articles_from_file():
    """Import articles from the CSV file"""
    app = create_app()
    
    with app.app_context():
        # Read the data file
        file_path = 'attached_assets/Pasted-DESIGNATION-REFERENCE-QUANTITE-PRIX-UNITAIRE-POMPE-FREIN-2559540302-2559540302-1-00-900-0000-SCOTC-1756304976142_1756304976144.txt'
        
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found")
            return False
            
        imported_count = 0
        skipped_count = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Skip the header line
                next(file)
                
                for line_num, line in enumerate(file, 2):
                    # Skip empty lines
                    if not line.strip():
                        continue
                        
                    # Split line by tabs
                    parts = line.strip().split('\t')
                    
                    # Skip malformed lines
                    if len(parts) < 4:
                        print(f"Line {line_num}: Skipping malformed line: {line.strip()[:100]}")
                        skipped_count += 1
                        continue
                    
                    designation = parts[0].strip()
                    reference = parts[1].strip()
                    
                    # Skip if designation is empty
                    if not designation:
                        skipped_count += 1
                        continue
                    
                    try:
                        quantite = float(parts[2].replace(',', '.'))
                        prix_unitaire = float(parts[3].replace(',', '.'))
                    except (ValueError, IndexError):
                        print(f"Line {line_num}: Invalid quantity or price: {line.strip()[:100]}")
                        skipped_count += 1
                        continue
                    
                    # Generate unique code_article
                    code_article = generate_code_article(designation, reference)
                    
                    # Check if article already exists
                    existing = Article.query.filter_by(code_article=code_article).first()
                    if existing:
                        # Update existing article stock and price
                        existing.stock_actuel = int(quantite)
                        existing.stock_initial = int(quantite)
                        existing.prix_unitaire = Decimal(str(prix_unitaire))
                        print(f"Updated existing article: {code_article}")
                    else:
                        # Create new article
                        article = Article(
                            code_article=code_article,
                            designation=designation,
                            categorie=determine_category(designation),
                            reference=reference if reference != designation else None,
                            stock_initial=int(quantite),
                            stock_actuel=int(quantite),
                            unite='pcs',
                            prix_unitaire=Decimal(str(prix_unitaire)),
                            seuil_minimum=max(1, int(quantite * 0.1))  # 10% of initial stock as minimum
                        )
                        
                        db.session.add(article)
                        imported_count += 1
                        
                    # Commit every 50 records to avoid memory issues
                    if (imported_count + skipped_count) % 50 == 0:
                        db.session.commit()
                        print(f"Processed {imported_count + skipped_count} lines...")
                
                # Final commit
                db.session.commit()
                
        except Exception as e:
            print(f"Error importing articles: {str(e)}")
            db.session.rollback()
            return False
        
        print(f"\nImport completed!")
        print(f"Articles imported: {imported_count}")
        print(f"Lines skipped: {skipped_count}")
        print(f"Total articles in database: {Article.query.count()}")
        
        return True

if __name__ == '__main__':
    print("Starting article import...")
    success = import_articles_from_file()
    
    if success:
        print("\n✅ Article import completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Article import failed!")
        sys.exit(1)