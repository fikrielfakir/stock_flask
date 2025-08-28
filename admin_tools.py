#!/usr/bin/env python3
"""
Admin Tools for StockCeramique License Management
Tools for administrators to manage licenses
"""

from license_manager import license_manager
import sqlite3
import json

def get_all_valid_licenses():
    """Get all valid license keys for admin purposes"""
    try:
        conn = sqlite3.connect(license_manager.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mac_address, license_data, activation_date, machine_name, is_active, checksum
            FROM licenses 
            ORDER BY activation_date DESC
        ''')
        
        licenses = []
        results = cursor.fetchall()
        
        for row in results:
            mac_address, license_data, activation_date, machine_name, is_active, checksum = row
            
            # Decrypt license key
            decrypted_key = license_manager._decrypt_data(license_data)
            
            if decrypted_key:
                # Generate expected key to verify validity
                expected_key = license_manager.generate_license_key(mac_address)
                is_valid = (decrypted_key == expected_key and 
                           license_manager._create_checksum(decrypted_key) == checksum)
                
                licenses.append({
                    'mac_address': mac_address,
                    'license_key': decrypted_key,
                    'activation_date': activation_date,
                    'machine_name': machine_name or 'Unknown',
                    'is_active': bool(is_active),
                    'is_valid': is_valid,
                    'status': 'Active' if is_active and is_valid else 'Inactive'
                })
        
        conn.close()
        return licenses
        
    except Exception as e:
        print(f"Error retrieving licenses: {e}")
        return []

def generate_license_for_mac(mac_address):
    """Generate a valid license key for a specific MAC address"""
    try:
        license_key = license_manager.generate_license_key(mac_address)
        return license_key
    except Exception as e:
        print(f"Error generating license: {e}")
        return None

def print_license_report():
    """Print a formatted report of all licenses"""
    licenses = get_all_valid_licenses()
    
    print("\n" + "="*80)
    print("STOCKCERAMIQUE LICENSE REPORT")
    print("="*80)
    
    if not licenses:
        print("No licenses found in database.")
        return
    
    print(f"Total licenses: {len(licenses)}")
    active_count = sum(1 for l in licenses if l['is_active'])
    print(f"Active licenses: {active_count}")
    print(f"Inactive licenses: {len(licenses) - active_count}")
    print("-"*80)
    
    for i, license_info in enumerate(licenses, 1):
        print(f"\n{i}. LICENSE ENTRY")
        print(f"   MAC Address: {license_info['mac_address']}")
        print(f"   License Key: {license_info['license_key']}")
        print(f"   Machine Name: {license_info['machine_name']}")
        print(f"   Activation Date: {license_info['activation_date']}")
        print(f"   Status: {license_info['status']}")
        print(f"   Valid: {'Yes' if license_info['is_valid'] else 'No'}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    print_license_report()