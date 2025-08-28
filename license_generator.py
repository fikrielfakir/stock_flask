#!/usr/bin/env python3
"""
License Key Generator for StockCeramique
Admin tool to generate one-time use license keys
"""

from onetime_license_manager import onetime_license_manager
import argparse

def generate_license_keys(count=10):
    """Generate a batch of one-time use license keys"""
    print(f"\n🔑 Generating {count} one-time use license keys...")
    print("="*60)
    
    keys = onetime_license_manager.generate_license_keys_batch(count)
    
    print(f"✅ Successfully generated {len(keys)} license keys:\n")
    
    for i, key in enumerate(keys, 1):
        print(f"{i:2d}. {key}")
    
    print("\n" + "="*60)
    print("📋 License keys have been stored in the database")
    print("🔒 Each key can only be used once for activation")
    print("\n")

def show_all_license_keys():
    """Show all generated license keys and their status"""
    licenses = onetime_license_manager.get_all_license_keys()
    
    print("\n" + "="*80)
    print("STOCKCERAMIQUE ONE-TIME LICENSE KEYS")
    print("="*80)
    
    if not licenses:
        print("No license keys found in database.")
        return
    
    total = len(licenses)
    used = sum(1 for l in licenses if l['is_used'])
    available = total - used
    
    print(f"Total license keys: {total}")
    print(f"Used license keys: {used}")
    print(f"Available license keys: {available}")
    print("-"*80)
    
    for i, license_info in enumerate(licenses, 1):
        status_icon = "🔴" if license_info['is_used'] else "🟢"
        print(f"\n{i:2d}. {status_icon} {license_info['license_key']} [{license_info['status']}]")
        
        if license_info['is_used']:
            print(f"     Used by: {license_info['used_by_machine']} ({license_info['used_by_mac']})")
            print(f"     Activated: {license_info['activation_date']}")
        else:
            print(f"     Created: {license_info['created_date']}")
    
    print("\n" + "="*80)
    print("🟢 = Available  🔴 = Used")
    print()

def show_available_keys_only():
    """Show only available (unused) license keys"""
    licenses = onetime_license_manager.get_all_license_keys()
    available_keys = [l for l in licenses if not l['is_used']]
    
    print("\n" + "="*60)
    print("AVAILABLE LICENSE KEYS")
    print("="*60)
    
    if not available_keys:
        print("No available license keys found.")
        print("Generate new keys using: python license_generator.py --generate 10")
        return
    
    print(f"Available license keys: {len(available_keys)}\n")
    
    for i, license_info in enumerate(available_keys, 1):
        print(f"{i:2d}. {license_info['license_key']}")
    
    print("\n" + "="*60)
    print("Each key can be used once for activation")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='StockCeramique License Key Generator')
    parser.add_argument('--generate', '-g', type=int, metavar='COUNT', 
                       help='Generate COUNT license keys (default: 10)')
    parser.add_argument('--list', '-l', action='store_true',
                       help='Show all license keys and their status')
    parser.add_argument('--available', '-a', action='store_true',
                       help='Show only available (unused) license keys')
    
    args = parser.parse_args()
    
    if args.generate:
        generate_license_keys(args.generate)
    elif args.list:
        show_all_license_keys()
    elif args.available:
        show_available_keys_only()
    else:
        # Default: show available keys
        show_available_keys_only()