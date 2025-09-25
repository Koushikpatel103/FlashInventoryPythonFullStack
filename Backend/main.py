#!/usr/bin/env python3
"""
FlashInventory - Complete Inventory Management System
"""

from Inventory_system import InventorySystem

def main():
    """Main application entry point"""
    print("🚀 Starting FlashInventory...")
    print("📦 Inventory Management System with Sales Tracking")
    print("=" * 50)
    
    try:
        inventory_system = InventorySystem()
        inventory_system.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Application interrupted by user.")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Please check your configuration and try again.")
    finally:
        print("👋 FlashInventory has been shut down.")

if __name__ == "__main__":
    main()