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
import base64

class LicenseManager:
    def __init__(self, db_path=None):
        # Use hidden/obfuscated database path
        if db_path is None:
            # Create hidden database in system directory with obfuscated name
            self.db_path = os.path.join(os.path.expanduser('~'), '.sys', 'cfg', 'app.dat')
        else:
            self.db_path = db_path
        self.ensure_db_exists()
        self.max_licenses = 1  # Limit to 1 license per installation
    
    def ensure_db_exists(self):
        """Create license database and table if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mac_address TEXT UNIQUE NOT NULL,
                license_data TEXT NOT NULL,
                activation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                machine_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                checksum TEXT
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
    
    def _encrypt_data(self, data):
        """Simple encryption for license data"""
        encoded = base64.b64encode(data.encode()).decode()
        # Add additional obfuscation
        obfuscated = ''.join(chr(ord(c) + 3) for c in encoded)
        return base64.b64encode(obfuscated.encode()).decode()
    
    def _decrypt_data(self, encrypted_data):
        """Decrypt license data"""
        try:
            decoded = base64.b64decode(encrypted_data.encode()).decode()
            deobfuscated = ''.join(chr(ord(c) - 3) for c in decoded)
            return base64.b64decode(deobfuscated.encode()).decode()
        except:
            return None
    
    def _create_checksum(self, data):
        """Create checksum for data integrity"""
        return hashlib.sha256(data.encode()).hexdigest()[:16]

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
    
    def check_license_limit(self):
        """Check if license limit has been reached"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM licenses WHERE is_active = TRUE')
        active_count = cursor.fetchone()[0]
        
        conn.close()
        return active_count < self.max_licenses

    def is_machine_licensed(self):
        """Check if the current machine is licensed"""
        current_mac = self.get_mac_address()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_data, is_active, checksum FROM licenses 
            WHERE mac_address = ? AND is_active = TRUE
        ''', (current_mac,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            license_data, is_active, checksum = result
            # Verify data integrity
            decrypted_key = self._decrypt_data(license_data)
            if decrypted_key and self._create_checksum(decrypted_key) == checksum:
                return True
        
        return False
    
    def activate_license(self, license_key):
        """Activate license for current machine"""
        current_mac = self.get_mac_address()
        machine_name = self.get_machine_name()
        
        # Validate license key
        if not self.validate_license_key(license_key, current_mac):
            return False, "Invalid license key for this machine"
        
        # Check license limits
        if not self.check_license_limit():
            return False, "License limit reached. Maximum activations exceeded."
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Encrypt license data
            encrypted_key = self._encrypt_data(license_key)
            checksum = self._create_checksum(license_key)
            
            # Check if this MAC is already licensed
            cursor.execute('SELECT id FROM licenses WHERE mac_address = ?', (current_mac,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing license
                cursor.execute('''
                    UPDATE licenses 
                    SET license_data = ?, is_active = TRUE, activation_date = CURRENT_TIMESTAMP, 
                        machine_name = ?, checksum = ?
                    WHERE mac_address = ?
                ''', (encrypted_key, machine_name, checksum, current_mac))
            else:
                # Insert new license
                cursor.execute('''
                    INSERT INTO licenses (mac_address, license_data, machine_name, checksum)
                    VALUES (?, ?, ?, ?)
                ''', (current_mac, encrypted_key, machine_name, checksum))
            
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
            SELECT license_data, activation_date, machine_name, is_active, checksum
            FROM licenses WHERE mac_address = ?
        ''', (current_mac,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            license_data, activation_date, machine_name, is_active, checksum = result
            decrypted_key = self._decrypt_data(license_data)
            
            # Verify integrity
            if decrypted_key and self._create_checksum(decrypted_key) == checksum:
                return {
                    'mac_address': current_mac,
                    'license_key': decrypted_key[:8] + '****',  # Partially mask the key
                    'activation_date': activation_date,
                    'machine_name': machine_name,
                    'is_active': bool(is_active)
                }
        return None
    
    def get_machine_identifier(self):
        """Get unique machine identifier for license generation"""
        mac = self.get_mac_address()
        return f"MAC: {mac}"

# Global license manager instance
license_manager = LicenseManager()