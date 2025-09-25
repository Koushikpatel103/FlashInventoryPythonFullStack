from product_manager import ProductManager
from sales_manager import SalesManager
from Display_utils import DisplayUtils

class InventorySystem:
    """Main system controller"""
    
    def __init__(self):
        self.product_manager = ProductManager()
        self.sales_manager = SalesManager()
        self.display_utils = DisplayUtils()
        self.running = True
    
    def run(self):
        """Main application loop"""
        print("🚀 Starting FlashInventory...")
        print("📦 Complete Inventory Management System")
        print("=" * 50)
        
        while self.running:
            self.show_dashboard()
            self.display_utils.display_main_menu()
            self.handle_main_menu()
    
    def show_dashboard(self):
        """Show dashboard summary"""
        try:
            products, _ = self.product_manager.get_all_products()
            low_stock, _ = self.product_manager.get_low_stock_products()
            sales_report, _ = self.sales_manager.get_sales_report(7)
            
            print(f"\n📊 DASHBOARD SUMMARY")
            print(f"   Total Products: {len(products) if products else 0}")
            print(f"   Low Stock Items: {len(low_stock) if low_stock else 0}")
            print(f"   Recent Sales (7 days): {sales_report.get('total_sales', 0)}")
            print(f"   Recent Revenue: ${sales_report.get('total_revenue', 0):.2f}")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error loading dashboard: {e}")
    
    def handle_main_menu(self):
        """Handle main menu selection"""
        choice = input("\nChoose an option (1-6): ").strip()
        
        if choice == '1':
            self.add_product_flow()
        elif choice == '2':
            self.view_all_products_flow()
        elif choice == '3':
            self.view_low_stock_flow()
        elif choice == '4':
            self.search_products_flow()
        elif choice == '5':
            self.sales_management_flow()
        elif choice == '6':
            self.exit_flow()
        else:
            print("❌ Invalid choice. Please enter 1-6.")
            self.display_utils.press_enter_to_continue()
    
    def add_product_flow(self):
        """Handle product addition"""
        product_data, error = self.display_utils.get_product_input()
        
        if error:
            print(f"❌ {error}")
        else:
            result, error = self.product_manager.add_product(**product_data)
            if error:
                print(f"❌ {error}")
            else:
                print(f"✅ Product '{product_data['name']}' added successfully!")
        
        self.display_utils.press_enter_to_continue()
    
    def view_all_products_flow(self):
        """Display all products"""
        products, error = self.product_manager.get_all_products()
        if error:
            print(f"❌ {error}")
        else:
            self.display_utils.display_products(products, "ALL PRODUCTS")
        self.display_utils.press_enter_to_continue()
    
    def view_low_stock_flow(self):
        """Display low stock products"""
        low_stock, error = self.product_manager.get_low_stock_products()
        if error:
            print(f"❌ {error}")
        else:
            if low_stock:
                self.display_utils.display_products(low_stock, "LOW STOCK ALERT")
            else:
                print("✅ All products have sufficient stock!")
        self.display_utils.press_enter_to_continue()
    
    def search_products_flow(self):
        """Handle product search"""
        search_term = input("\n🔍 Enter product name or SKU to search: ").strip()
        
        if search_term:
            results, error = self.product_manager.search_products(search_term)
            if error:
                print(f"❌ {error}")
            else:
                if results:
                    self.display_utils.display_products(results, f"SEARCH RESULTS FOR '{search_term}'")
                else:
                    print(f"🔍 No products found matching '{search_term}'")
        else:
            print("❌ Please enter a search term.")
        
        self.display_utils.press_enter_to_continue()
    
    def sales_management_flow(self):
        """Sales management menu"""
        while True:
            self.display_utils.display_sales_menu()
            choice = input("\nChoose sales option (1-4): ").strip()
            
            if choice == '1':
                self.record_sale_flow()
            elif choice == '2':
                self.view_sales_report_flow()
            elif choice == '3':
                self.view_recent_sales_flow()
            elif choice == '4':
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                self.display_utils.press_enter_to_continue()
    
    def record_sale_flow(self):
        """Record a new sale"""
        sale_data, error = self.display_utils.get_sale_input()
        
        if error:
            print(f"❌ {error}")
        else:
            # Get product by SKU
            product, error = self.product_manager.get_product_by_sku(sale_data['product_sku'])
            if error or not product:
                print("❌ Product not found! Please check the SKU.")
            else:
                # Check stock
                if product['stock_quantity'] < sale_data['quantity']:
                    print(f"❌ Not enough stock! Available: {product['stock_quantity']}")
                else:
                    # Record sale
                    sale, error = self.sales_manager.record_sale(
                        product['id'], 
                        sale_data['quantity'], 
                        sale_data['sale_price']
                    )
                    
                    if error:
                        print(f"❌ {error}")
                    else:
                        # Update stock
                        new_stock = product['stock_quantity'] - sale_data['quantity']
                        _, error = self.product_manager.update_stock(product['id'], new_stock)
                        
                        if error:
                            print(f"✅ Sale recorded but stock update failed: {error}")
                        else:
                            total = sale_data['quantity'] * (sale_data['sale_price'] or product['price'])
                            print(f"✅ Sale recorded! Total: ${total:.2f}")
                            print(f"📦 New stock level: {new_stock}")
        
        self.display_utils.press_enter_to_continue()
    
    def view_sales_report_flow(self):
        """Display sales report"""
        try:
            days = int(input("Report period in days (default 30): ") or "30")
            report, error = self.sales_manager.get_sales_report(days)
            if error:
                print(f"❌ {error}")
            else:
                self.display_utils.display_sales_report(report)
        except ValueError:
            print("❌ Please enter a valid number of days.")
        
        self.display_utils.press_enter_to_continue()
    
    def view_recent_sales_flow(self):
        """Display recent sales"""
        try:
            limit = int(input("Number of recent sales to show (default 10): ") or "10")
            sales, error = self.sales_manager.get_recent_sales(limit)
            if error:
                print(f"❌ {error}")
            else:
                self.display_utils.display_sales(sales, f"LAST {limit} SALES")
        except ValueError:
            print("❌ Please enter a valid number.")
        
        self.display_utils.press_enter_to_continue()
    
    def exit_flow(self):
        """Handle application exit"""
        print("\n👋 Thank you for using FlashInventory!")
        print("📊 Your data is safely stored in the cloud.")
        self.running = False