#!/usr/bin/env python3
"""
One-Time License Manager for StockCeramique
Handles one-time use license keys that can be activated once on any machine
"""

import hashlib
import uuid
import sqlite3
import os
from datetime import datetime
import secrets
import string
import base64

class OneTimeLicenseManager:
    def __init__(self, db_path=None):
        # Use hidden database path
        if db_path is None:
            self.db_path = os.path.join(os.path.expanduser('~'), '.sys', 'cfg', 'licenses.dat')
        else:
            self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Create license database and tables if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # One-time license keys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS onetime_licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_key TEXT UNIQUE NOT NULL,
                is_used BOOLEAN DEFAULT FALSE,
                used_by_mac TEXT,
                used_by_machine TEXT,
                activation_date TIMESTAMP,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                checksum TEXT
            )
        ''')
        
        # Activated machines table (for the old MAC-based system)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activated_machines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mac_address TEXT UNIQUE NOT NULL,
                license_key TEXT NOT NULL,
                machine_name TEXT,
                activation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_mac_address(self):
        """Get the primary MAC address of the machine"""
        try:
            import psutil
            interfaces = psutil.net_if_addrs()
            
            for interface_name, interface_addresses in interfaces.items():
                if interface_name.lower() != 'lo' and interface_name.lower() != 'loopback':
                    for address in interface_addresses:
                        if address.family == psutil.AF_LINK:
                            mac = address.address
                            if mac and mac != '00:00:00:00:00:00':
                                return mac.upper()
            
            return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0,2*6,2)][::-1]).upper()
        except Exception as e:
            return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0,2*6,2)][::-1]).upper()
    
    def get_machine_name(self):
        """Get the machine name/hostname"""
        try:
            return os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME', 'Unknown'))
        except:
            return 'Unknown'
    
    def _create_checksum(self, data):
        """Create checksum for data integrity"""
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def generate_license_key(self):
        """Generate a random one-time use license key"""
        # Generate random license key
        chars = string.ascii_uppercase + string.digits
        # Remove confusing characters
        chars = chars.replace('0', '').replace('O', '').replace('I', '').replace('L', '')
        
        key_parts = []
        for _ in range(4):
            part = ''.join(secrets.choice(chars) for _ in range(4))
            key_parts.append(part)
        
        return '-'.join(key_parts)
    
    def generate_license_keys_batch(self, count=10):
        """Generate a batch of one-time use license keys"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        generated_keys = []
        
        for _ in range(count):
            # Generate unique key
            while True:
                license_key = self.generate_license_key()
                
                # Check if key already exists
                cursor.execute('SELECT id FROM onetime_licenses WHERE license_key = ?', (license_key,))
                if not cursor.fetchone():
                    break
            
            # Create checksum
            checksum = self._create_checksum(license_key)
            
            # Insert into database
            cursor.execute('''
                INSERT INTO onetime_licenses (license_key, checksum)
                VALUES (?, ?)
            ''', (license_key, checksum))
            
            generated_keys.append(license_key)
        
        conn.commit()
        conn.close()
        
        return generated_keys
    
    def is_license_key_valid(self, license_key):
        """Check if a license key exists and is valid"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_key, is_used, checksum FROM onetime_licenses 
            WHERE license_key = ?
        ''', (license_key.strip().upper(),))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            stored_key, is_used, checksum = result
            # Verify checksum
            if self._create_checksum(stored_key) == checksum:
                return True, is_used
        
        return False, False
    
    def activate_license_key(self, license_key):
        """Activate a one-time license key"""
        license_key = license_key.strip().upper()
        current_mac = self.get_mac_address()
        machine_name = self.get_machine_name()
        
        # Check if license key is valid
        is_valid, is_used = self.is_license_key_valid(license_key)
        
        if not is_valid:
            return False, "Invalid license key"
        
        if is_used:
            return False, "This license key has already been used. Contact support for assistance."
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Mark license as used
            cursor.execute('''
                UPDATE onetime_licenses 
                SET is_used = TRUE, used_by_mac = ?, used_by_machine = ?, activation_date = CURRENT_TIMESTAMP
                WHERE license_key = ?
            ''', (current_mac, machine_name, license_key))
            
            # Also record in activated machines table
            cursor.execute('''
                INSERT OR REPLACE INTO activated_machines (mac_address, license_key, machine_name)
                VALUES (?, ?, ?)
            ''', (current_mac, license_key, machine_name))
            
            conn.commit()
            conn.close()
            
            return True, "License activated successfully"
            
        except Exception as e:
            return False, f"Database error: {str(e)}"
    
    def is_machine_licensed(self):
        """Check if the current machine has an active license"""
        current_mac = self.get_mac_address()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_key FROM activated_machines 
            WHERE mac_address = ? AND is_active = TRUE
        ''', (current_mac,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    def get_machine_license_info(self):
        """Get license information for current machine"""
        current_mac = self.get_mac_address()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_key, activation_date, machine_name
            FROM activated_machines 
            WHERE mac_address = ? AND is_active = TRUE
        ''', (current_mac,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            license_key, activation_date, machine_name = result
            return {
                'mac_address': current_mac,
                'license_key': license_key[:8] + '****',  # Partially mask
                'activation_date': activation_date,
                'machine_name': machine_name,
                'is_active': True
            }
        return None
    
    def deactivate_license(self):
        """Deactivate license for current machine"""
        current_mac = self.get_mac_address()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE activated_machines SET is_active = FALSE 
            WHERE mac_address = ?
        ''', (current_mac,))
        
        conn.commit()
        conn.close()
    
    def get_all_license_keys(self):
        """Get all generated license keys (for admin purposes)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_key, is_used, used_by_mac, used_by_machine, activation_date, created_date
            FROM onetime_licenses 
            ORDER BY created_date DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        licenses = []
        for row in results:
            license_key, is_used, used_by_mac, used_by_machine, activation_date, created_date = row
            licenses.append({
                'license_key': license_key,
                'is_used': bool(is_used),
                'used_by_mac': used_by_mac or 'Not used',
                'used_by_machine': used_by_machine or 'Not used',
                'activation_date': activation_date or 'Not activated',
                'created_date': created_date,
                'status': 'Used' if is_used else 'Available'
            })
        
        return licenses

# Global instance
onetime_license_manager = OneTimeLicenseManager()