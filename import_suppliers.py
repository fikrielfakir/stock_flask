#!/usr/bin/env python3
"""
Script to import supplier data from the provided text file
"""

import re
import os
import sys
from flask_app import create_app
from flask_models import db, Supplier
from datetime import datetime

def clean_phone_number(phone):
    """Clean and normalize phone numbers"""
    if not phone or phone in ['0', '00', '000', '0000', '00000', '000000', '0000000', '00000000', '000000000', '0000000000', '00000000000']:
        return None
    
    # Remove spaces and clean formatting
    phone = re.sub(r'[^\d+]', '', str(phone))
    
    # If it's just zeros, return None
    if re.match(r'^0+$', phone):
        return None
        
    return phone if phone else None

def clean_email(email):
    """Clean and validate email addresses"""
    if not email or email.strip() == '':
        return None
    
    email = email.strip()
    
    # Basic email validation
    if '@' in email and '.' in email:
        return email
    
    return None

def parse_supplier_line(line):
    """Parse a single line of supplier data"""
    if not line or line.startswith('_F') or len(line.strip()) < 10:
        return None
    
    # Split by tabs
    parts = line.split('\t')
    
    if len(parts) < 6:
        return None
    
    nom = parts[0].strip() if parts[0] else None
    adresse = parts[1].strip() if parts[1] else None
    telephone = clean_phone_number(parts[2]) if parts[2] else None
    fax = clean_phone_number(parts[3]) if parts[3] else None
    email = clean_email(parts[4]) if parts[4] else None
    
    # Skip if no name
    if not nom or nom == '':
        return None
    
    # Create supplier data
    supplier_data = {
        'nom': nom,
        'adresse': adresse,
        'telephone': telephone,
        'email': email,
        'contact': None,  # We'll use the main phone as contact if available
        'conditions_paiement': None,
        'delai_livraison': None
    }
    
    return supplier_data

def import_suppliers_from_file(file_path):
    """Import suppliers from the text file"""
    app = create_app()
    
    with app.app_context():
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            imported_count = 0
            skipped_count = 0
            
            print(f"Processing {len(lines)} lines...")
            
            for line_num, line in enumerate(lines, 1):
                supplier_data = parse_supplier_line(line)
                
                if not supplier_data:
                    skipped_count += 1
                    continue
                
                # Check if supplier already exists
                existing = Supplier.query.filter_by(nom=supplier_data['nom']).first()
                if existing:
                    print(f"Supplier '{supplier_data['nom']}' already exists, skipping...")
                    skipped_count += 1
                    continue
                
                try:
                    # Create new supplier
                    supplier = Supplier(
                        nom=supplier_data['nom'],
                        adresse=supplier_data['adresse'],
                        telephone=supplier_data['telephone'],
                        email=supplier_data['email'],
                        contact=supplier_data['contact'],
                        conditions_paiement=supplier_data['conditions_paiement'],
                        delai_livraison=supplier_data['delai_livraison']
                    )
                    
                    db.session.add(supplier)
                    imported_count += 1
                    
                    if imported_count % 50 == 0:
                        print(f"Processed {imported_count} suppliers...")
                        
                except Exception as e:
                    print(f"Error creating supplier '{supplier_data['nom']}': {str(e)}")
                    skipped_count += 1
                    continue
            
            # Commit all changes
            db.session.commit()
            
            print(f"\nImport completed!")
            print(f"Successfully imported: {imported_count} suppliers")
            print(f"Skipped: {skipped_count} entries")
            
            return imported_count, skipped_count
            
        except Exception as e:
            print(f"Error during import: {str(e)}")
            db.session.rollback()
            return 0, 0

if __name__ == '__main__':
    file_path = 'attached_assets/Pasted--F-ADRESSE-F-TEL-F-FAX-F-EMAIL-F-ID-D-REMARQUE-F-A-D-S-INDUSTRIE-MAROC-0539714269-1-FERAILLE-SI-1756416297250_1756416297251.txt'
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    imported, skipped = import_suppliers_from_file(file_path)
    print(f"\nFinal result: {imported} imported, {skipped} skipped")