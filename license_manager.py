#!/usr/bin/env python3
"""
License Manager for StockCeramique
Handles software licensing, MAC address detection, and activation
"""

import hashlib
import uuid
import sqlite3
import os
from datetime import datetime, timedelta
import psutil
import json

class LicenseManager:
    def __init__(self, db_path='instance/license.db'):
        self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Create license database and table if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mac_address TEXT UNIQUE NOT NULL,
                license_key TEXT NOT NULL,
                activation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                machine_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_mac_address(self):
        """Get the primary MAC address of the machine"""
        try:
            # Get all network interfaces
            interfaces = psutil.net_if_addrs()
            
            # Look for the primary active interface (not loopback)
            for interface_name, interface_addresses in interfaces.items():
                if interface_name.lower() != 'lo' and interface_name.lower() != 'loopback':
                    for address in interface_addresses:
                        if address.family == psutil.AF_LINK:  # MAC address
                            mac = address.address
                            if mac and mac != '00:00:00:00:00:00':
                                return mac.upper()
            
            # Fallback: get MAC address of any interface
            return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0,2*6,2)][::-1]).upper()
        except Exception as e:
            # Ultimate fallback
            return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0,2*6,2)][::-1]).upper()
    
    def get_machine_name(self):
        """Get the machine name/hostname"""
        try:
            return os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME', 'Unknown'))
        except:
            return 'Unknown'
    
    def generate_license_key(self, mac_address, secret_seed="StockCeramique2025"):
        """Generate a license key based on MAC address"""
        # Create a hash using MAC address and secret
        data = f"{mac_address}{secret_seed}".encode()
        hash_obj = hashlib.sha256(data)
        hex_dig = hash_obj.hexdigest()
        
        # Format as a license key: XXXX-XXXX-XXXX-XXXX
        key_parts = [hex_dig[i:i+4].upper() for i in range(0, 16, 4)]
        return '-'.join(key_parts)
    
    def validate_license_key(self, license_key, mac_address):
        """Validate if the license key is correct for the MAC address"""
        expected_key = self.generate_license_key(mac_address)
        return license_key.strip().upper() == expected_key
    
    def is_machine_licensed(self):
        """Check if the current machine is licensed"""
        current_mac = self.get_mac_address()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_key, is_active FROM licenses 
            WHERE mac_address = ? AND is_active = TRUE
        ''', (current_mac,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    def activate_license(self, license_key):
        """Activate license for current machine"""
        current_mac = self.get_mac_address()
        machine_name = self.get_machine_name()
        
        # Validate license key
        if not self.validate_license_key(license_key, current_mac):
            return False, "Invalid license key for this machine"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if this MAC is already licensed
            cursor.execute('SELECT id FROM licenses WHERE mac_address = ?', (current_mac,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing license
                cursor.execute('''
                    UPDATE licenses 
                    SET license_key = ?, is_active = TRUE, activation_date = CURRENT_TIMESTAMP, machine_name = ?
                    WHERE mac_address = ?
                ''', (license_key, machine_name, current_mac))
            else:
                # Insert new license
                cursor.execute('''
                    INSERT INTO licenses (mac_address, license_key, machine_name)
                    VALUES (?, ?, ?)
                ''', (current_mac, license_key, machine_name))
            
            conn.commit()
            conn.close()
            return True, "License activated successfully"
            
        except Exception as e:
            return False, f"Database error: {str(e)}"
    
    def deactivate_license(self):
        """Deactivate license for current machine"""
        current_mac = self.get_mac_address()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE licenses SET is_active = FALSE 
            WHERE mac_address = ?
        ''', (current_mac,))
        
        conn.commit()
        conn.close()
    
    def get_license_info(self):
        """Get license information for current machine"""
        current_mac = self.get_mac_address()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_key, activation_date, machine_name, is_active
            FROM licenses WHERE mac_address = ?
        ''', (current_mac,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'mac_address': current_mac,
                'license_key': result[0],
                'activation_date': result[1],
                'machine_name': result[2],
                'is_active': bool(result[3])
            }
        return None
    
    def get_machine_identifier(self):
        """Get unique machine identifier for license generation"""
        mac = self.get_mac_address()
        return f"MAC: {mac}"

# Global license manager instance
license_manager = LicenseManager()