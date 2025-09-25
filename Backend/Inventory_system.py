from product_manager import ProductManager
from sales_manager import SalesManager
from Display_utils import DisplayUtils

class InventorySystem:
    """
    Main system controller - manages the entire application flow
    """
    
    def __init__(self):
        self.product_manager = ProductManager()
        self.sales_manager = SalesManager()
        self.display_utils = DisplayUtils()
        self.running = True
    
    def test_connection(self):
        """Test database connection"""
        success, message = self.product_manager.db.test_connection()
        print(message)
        return success
    
    def run(self):
        """Main application loop"""
        if not self.test_connection():
            print("❌ Cannot start application. Please check your configuration.")
            return
        
        print("✅ FlashInventory started successfully!")
        
        while self.running:
            self.display_utils.clear_screen()
            self.show_dashboard()
            self.display_utils.display_main_menu()
            self.handle_main_menu_choice()
    
    def show_dashboard(self):
        """Show dashboard summary"""
        products, _ = self.product_manager.get_all_products()
        low_stock, _ = self.product_manager.get_low_stock_products()
        recent_sales, _ = self.sales_manager.get_recent_sales(5)
        sales_report, _ = self.sales_manager.get_sales_report(7)
        
        print(f"\n📊 DASHBOARD SUMMARY")
        print(f"   Total Products: {len(products)}")
        print(f"   Low Stock Items: {len(low_stock)}")
        print(f"   Recent Sales (7 days): {sales_report['total_sales']} transactions")
        print(f"   Recent Revenue: ${sales_report['total_revenue']:.2f}")
    
    def handle_main_menu_choice(self):
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
    
    # PRODUCT MANAGEMENT FLOWS
    def add_product_flow(self):
        """Handle product addition"""
        self.display_utils.clear_screen()
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
        self.display_utils.clear_screen()
        products, error = self.product_manager.get_all_products()
        if error:
            print(f"❌ {error}")
        else:
            self.display_utils.display_products(products, "ALL PRODUCTS")
        self.display_utils.press_enter_to_continue()
    
    def view_low_stock_flow(self):
        """Display low stock products"""
        self.display_utils.clear_screen()
        low_stock, error = self.product_manager.get_low_stock_products()
        if error:
            print(f"❌ {error}")
        else:
            if low_stock:
                self.display_utils.display_products(low_stock, "LOW STOCK ALERT")
                print(f"⚠️  {len(low_stock)} product(s) need restocking!")
            else:
                print("✅ All products have sufficient stock!")
        self.display_utils.press_enter_to_continue()
    
    def search_products_flow(self):
        """Handle product search"""
        self.display_utils.clear_screen()
        search_term = self.display_utils.get_search_term()
        
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
    
    # SALES MANAGEMENT FLOWS
    def sales_management_flow(self):
        """Sales management menu"""
        while True:
            self.display_utils.clear_screen()
            self.display_utils.display_sales_menu()
            
            choice = input("\nChoose sales option (1-5): ").strip()
            
            if choice == '1':
                self.record_sale_flow()
            elif choice == '2':
                self.view_sales_report_flow()
            elif choice == '3':
                self.view_recent_sales_flow()
            elif choice == '4':
                self.view_daily_sales_flow()
            elif choice == '5':
                break  # Back to main menu
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                self.display_utils.press_enter_to_continue()
    
    def record_sale_flow(self):
        """Record a new sale"""
        self.display_utils.clear_screen()
        sale_data, error = self.display_utils.get_sale_input()
        
        if error:
            print(f"❌ {error}")
        else:
            # Get product by SKU
            product, error = self.product_manager.get_product_by_sku(sale_data['product_sku'])
            if error or not product:
                print("❌ Product not found! Please check the SKU.")
            else:
                # Check stock availability
                if product['stock_quantity'] < sale_data['quantity']:
                    print(f"❌ Not enough stock! Available: {product['stock_quantity']}, Requested: {sale_data['quantity']}")
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
                        print("✅ Sale recorded successfully!")
                        
                        # Update stock
                        new_stock = product['stock_quantity'] - sale_data['quantity']
                        _, error = self.product_manager.update_stock(product['id'], new_stock)
                        if error:
                            print(f"⚠️  Sale recorded but stock update failed: {error}")
        
        self.display_utils.press_enter_to_continue()
    
    def view_sales_report_flow(self):
        """Display sales report"""
        self.display_utils.clear_screen()
        
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
        self.display_utils.clear_screen()
        
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
    
    def view_daily_sales_flow(self):
        """Display daily sales breakdown"""
        self.display_utils.clear_screen()
        
        try:
            days = int(input("Number of days to show (default 7): ") or "7")
            daily_sales, error = self.sales_manager.get_daily_sales(days)
            if error:
                print(f"❌ {error}")
            else:
                self.display_utils.display_daily_sales(daily_sales)
        except ValueError:
            print("❌ Please enter a valid number of days.")
        
        self.display_utils.press_enter_to_continue()
    
    def exit_flow(self):
        """Handle application exit"""
        print("\n👋 Thank you for using FlashInventory!")
        print("📊 Your data is safely stored in the cloud.")
        self.running = False