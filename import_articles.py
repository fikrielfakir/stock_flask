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
        file_path = 'attached_assets/da_1756417109268.txt'
        
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found")
            return False
            
        imported_count = 0
        skipped_count = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Skip the header line (NOM_P   Designation_P)
                next(file)
                
                for line_num, line in enumerate(file, 2):
                    # Skip empty lines
                    if not line.strip():
                        continue
                        
                    # Split line by tabs - expecting NOM_P and Designation_P
                    parts = line.strip().split('\t', 1)  # Only split into 2 parts max
                    
                    # Skip malformed lines (need at least 2 parts)
                    if len(parts) < 2:
                        print(f"Line {line_num}: Skipping malformed line: {line.strip()[:100]}")
                        skipped_count += 1
                        continue
                    
                    code_article = parts[0].strip()  # NOM_P becomes the article code
                    designation = parts[1].strip()   # Designation_P becomes the designation
                    
                    # Skip if either code or designation is empty
                    if not code_article or not designation:
                        print(f"Line {line_num}: Skipping empty code or designation: {line.strip()[:100]}")
                        skipped_count += 1
                        continue
                    
                    # Check if article already exists
                    existing = Article.query.filter_by(code_article=code_article).first()
                    if existing:
                        # Update existing article designation if it's different
                        if existing.designation != designation:
                            existing.designation = designation
                            print(f"Updated existing article: {code_article}")
                        else:
                            print(f"Skipped duplicate article: {code_article}")
                        skipped_count += 1
                    else:
                        # Create new article with default values
                        article = Article(
                            code_article=code_article,
                            designation=designation,
                            categorie=determine_category(designation),
                            reference=None,  # No reference data in this file
                            stock_initial=0,  # Default stock
                            stock_actuel=0,   # Default stock
                            unite='pcs',      # Default unit
                            prix_unitaire=None,  # No price data in this file
                            seuil_minimum=5   # Default minimum threshold
                        )
                        
                        db.session.add(article)
                        imported_count += 1
                        
                        if imported_count % 100 == 0:
                            print(f"Imported {imported_count} articles...")
                        
                    # Commit every 100 records to avoid memory issues
                    if (imported_count + skipped_count) % 100 == 0:
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