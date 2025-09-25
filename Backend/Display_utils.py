class DisplayUtils:
    """
    Handles all display and formatting operations
    """
    
    @staticmethod
    def display_products(products, title="PRODUCT INVENTORY"):
        """Display products in formatted table"""
        if not products:
            print(f"\n📭 No products found for '{title}'")
            return
        
        print(f"\n📦 {title}")
        print("=" * 95)
        print(f"{'Status':8} | {'Name':20} | {'Price':8} | {'Stock':6} | {'Category':12} | SKU")
        print("=" * 95)
        
        for product in products:
            stock = product.get('stock_quantity', 0)
            min_stock = product.get('min_stock_level', 5)
            
            # Determine status
            if stock == 0:
                status = "🔴 OUT"
            elif stock < min_stock:
                status = "🟡 LOW"
            else:
                status = "🟢 OK "
            
            name = product.get('name', 'Unknown')[:20]
            price = product.get('price', 0)
            category = product.get('category', 'General')[:12]
            sku = product.get('sku', 'N/A')
            
            print(f"{status:8} | {name:20} | ${price:7.2f} | {stock:6} | {category:12} | {sku}")
        
        print("=" * 95)
        print(f"Total products: {len(products)}")
    
    @staticmethod
    def display_sales(sales, title="SALES HISTORY"):
        """Display sales in formatted table"""
        if not sales:
            print(f"\n💸 No sales records found for '{title}'")
            return
        
        print(f"\n💰 {title}")
        print("=" * 85)
        print(f"{'Date':12} | {'Product':20} | {'Qty':4} | {'Price':8} | {'Total':10}")
        print("=" * 85)
        
        total_revenue = 0
        for sale in sales:
            # Extract date (YYYY-MM-DD)
            sale_date = sale['sale_date'][:10] if 'sale_date' in sale else 'Unknown'
            
            # Get product name
            if 'products' in sale and sale['products']:
                product_name = sale['products'].get('name', 'Unknown')[:20]
                sku = sale['products'].get('sku', 'N/A')
                product_display = f"{product_name} ({sku})"
            else:
                product_display = "Unknown Product"
            
            quantity = sale.get('quantity_sold', 0)
            price = sale.get('sale_price', 0)
            total = quantity * price
            total_revenue += total
            
            print(f"{sale_date:12} | {product_display:20} | {quantity:4} | ${price:7.2f} | ${total:9.2f}")
        
        print("=" * 85)
        print(f"Total revenue: ${total_revenue:.2f}")
        print(f"Total transactions: {len(sales)}")
    
    @staticmethod
    def display_sales_report(report):
        """Display sales report"""
        print("\n📊 SALES REPORT")
        print("=" * 50)
        print(f"Period: {report['start_date']} to {report['end_date']}")
        print(f"Total Sales: {report['total_sales']} transactions")
        print(f"Items Sold: {report['total_items_sold']} units")
        print(f"Total Revenue: ${report['total_revenue']:.2f}")
        print(f"Average Sale: ${report['average_sale_value']:.2f}")
        print("=" * 50)
    
    @staticmethod
    def display_daily_sales(daily_sales):
        """Display daily sales breakdown"""
        if not daily_sales:
            print("\n💸 No daily sales data available")
            return
        
        print("\n📅 DAILY SALES BREAKDOWN")
        print("=" * 60)
        print(f"{'Date':12} | {'Sales':6} | {'Items':6} | {'Revenue':10}")
        print("=" * 60)
        
        for day in daily_sales:
            print(f"{day['date']:12} | {day['total_sales']:6} | {day['items_sold']:6} | ${day['total_revenue']:9.2f}")
        
        print("=" * 60)
    
    @staticmethod
    def display_main_menu():
        """Display main menu"""
        print("\n" + "="*50)
        print("🏪 FLASH INVENTORY MANAGEMENT SYSTEM")
        print("="*50)
        print("1. 📥 Add New Product")
        print("2. 📋 View All Products")
        print("3. ⚠️  View Low Stock Products")
        print("4. 🔍 Search Products")
        print("5. 💰 Sales Management")
        print("6. 🚪 Exit")
        print("="*50)
    
    @staticmethod
    def display_sales_menu():
        """Display sales menu"""
        print("\n" + "="*40)
        print("💰 SALES MANAGEMENT")
        print("="*40)
        print("1. 💳 Record Sale")
        print("2. 📊 Sales Report")
        print("3. 📈 Recent Sales")
        print("4. 📅 Daily Sales")
        print("5. ↩️  Back to Main Menu")
        print("="*40)
    
    @staticmethod
    def get_product_input():
        """Get product input from user"""
        try:
            print("\n➕ ADD NEW PRODUCT")
            print("-" * 30)
            
            name = input("Product name: ").strip()
            if not name:
                return None, "Product name is required!"
            
            sku = input("SKU (unique code): ").strip()
            if not sku:
                return None, "SKU is required!"
            
            try:
                price = float(input("Price: $").strip())
                if price <= 0:
                    return None, "Price must be greater than 0!"
            except ValueError:
                return None, "Please enter a valid price!"
            
            try:
                stock = int(input("Initial stock quantity: ").strip())
                if stock < 0:
                    return None, "Stock cannot be negative!"
            except ValueError:
                return None, "Please enter a valid stock quantity!"
            
            category = input("Category (press Enter for 'General'): ").strip()
            category = category if category else "General"
            
            description = input("Description (optional): ").strip()
            
            return {
                'name': name,
                'sku': sku,
                'price': price,
                'stock': stock,
                'category': category,
                'description': description
            }, None
            
        except KeyboardInterrupt:
            return None, "Input cancelled."
    
    @staticmethod
    def get_sale_input():
        """Get sale input from user"""
        try:
            print("\n💳 RECORD A SALE")
            print("-" * 30)
            
            product_sku = input("Product SKU: ").strip()
            if not product_sku:
                return None, "Product SKU is required!"
            
            try:
                quantity = int(input("Quantity sold: ").strip())
                if quantity <= 0:
                    return None, "Quantity must be greater than 0!"
            except ValueError:
                return None, "Please enter a valid quantity!"
            
            try:
                custom_price = input("Sale price (press Enter for listed price): ").strip()
                sale_price = float(custom_price) if custom_price else None
                if sale_price and sale_price <= 0:
                    return None, "Sale price must be greater than 0!"
            except ValueError:
                return None, "Please enter a valid price!"
            
            return {
                'product_sku': product_sku,
                'quantity': quantity,
                'sale_price': sale_price
            }, None
            
        except KeyboardInterrupt:
            return None, "Input cancelled."
    
    @staticmethod
    def get_search_term():
        """Get search term from user"""
        term = input("\n🔍 Enter product name or SKU to search: ").strip()
        return term if term else None
    
    @staticmethod
    def press_enter_to_continue():
        """Wait for user to press Enter"""
        input("\nPress Enter to continue...")
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')