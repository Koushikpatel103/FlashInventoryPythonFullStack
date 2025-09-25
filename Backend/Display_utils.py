class DisplayUtils:
    """Handles all display formatting"""
    
    @staticmethod
    def display_products(products, title="PRODUCT INVENTORY"):
        """Display products in formatted table"""
        if not products:
            print(f"\n📭 No products found")
            return
        
        print(f"\n📦 {title}")
        print("=" * 80)
        print(f"{'Status':<4} {'Name':<20} {'Price':<10} {'Stock':<8} {'Category':<12} SKU")
        print("=" * 80)
        
        for product in products:
            stock = product.get('stock_quantity', 0)
            min_stock = product.get('min_stock_level', 5)
            
            # Determine status
            if stock == 0:
                status = "🔴"
            elif stock < min_stock:
                status = "🟡"
            else:
                status = "🟢"
            
            name = product.get('name', 'Unknown')[:19]
            price = product.get('price', 0)
            category = product.get('category', 'General')[:11]
            sku = product.get('sku', 'N/A')
            
            print(f"{status:<4} {name:<20} ${price:<9.2f} {stock:<8} {category:<12} {sku}")
        
        print("=" * 80)
        print(f"Total products: {len(products)}")
    
    @staticmethod
    def display_sales(sales, title="SALES HISTORY"):
        """Display sales in formatted table"""
        if not sales:
            print(f"\n💸 No sales records found")
            return
        
        print(f"\n💰 {title}")
        print("=" * 70)
        print(f"{'Date':<12} {'Product':<20} {'Qty':<4} {'Price':<8} {'Total':<10}")
        print("=" * 70)
        
        total_revenue = 0
        for sale in sales:
            sale_date = sale['sale_date'][:10]  # YYYY-MM-DD
            
            # Get product info
            product_info = sale.get('products', {})
            product_name = product_info.get('name', 'Unknown')[:19]
            sku = product_info.get('sku', 'N/A')
            product_display = f"{product_name} ({sku})"
            
            quantity = sale.get('quantity_sold', 0)
            price = sale.get('sale_price', 0)
            total = quantity * price
            total_revenue += total
            
            print(f"{sale_date:<12} {product_display:<20} {quantity:<4} ${price:<7.2f} ${total:<9.2f}")
        
        print("=" * 70)
        print(f"Total revenue: ${total_revenue:.2f}")
        print(f"Total transactions: {len(sales)}")
    
    @staticmethod
    def display_sales_report(report):
        """Display sales report"""
        print("\n📊 SALES REPORT")
        print("=" * 50)
        print(f"Report Period: {report['period_days']} days")
        print(f"Total Sales: {report['total_sales']} transactions")
        print(f"Items Sold: {report['total_items_sold']} units")
        print(f"Total Revenue: ${report['total_revenue']:.2f}")
        print(f"Average Sale: ${report['average_sale_value']:.2f}")
        print("=" * 50)
    
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
        print("4. ↩️  Back to Main Menu")
        print("="*40)
    
    @staticmethod
    def get_product_input():
        """Get product input from user"""
        try:
            print("\n➕ ADD NEW PRODUCT")
            print("-" * 30)
            
            name = input("Product name: ").strip()
            if not name:
                return None, "Product name is required"
            
            sku = input("SKU (unique code): ").strip()
            if not sku:
                return None, "SKU is required"
            
            try:
                price = float(input("Price: $").strip())
                if price <= 0:
                    return None, "Price must be greater than 0"
            except ValueError:
                return None, "Please enter a valid price"
            
            try:
                initial_stock = int(input("Initial stock quantity: ").strip())
                if initial_stock < 0:
                    return None, "Stock cannot be negative"
            except ValueError:
                return None, "Please enter a valid stock quantity"
            
            category = input("Category (press Enter for 'General'): ").strip()
            category = category if category else "General"
            
            description = input("Description (optional): ").strip()
            
            return {
                'name': name,
                'sku': sku,
                'price': price,
                'initial_stock': initial_stock,
                'category': category,
                'description': description
            }, None
            
        except KeyboardInterrupt:
            return None, "Input cancelled"
    
    @staticmethod
    def get_sale_input():
        """Get sale input from user"""
        try:
            print("\n💳 RECORD A SALE")
            print("-" * 30)
            
            product_sku = input("Product SKU: ").strip()
            if not product_sku:
                return None, "Product SKU is required"
            
            try:
                quantity = int(input("Quantity sold: ").strip())
                if quantity <= 0:
                    return None, "Quantity must be greater than 0"
            except ValueError:
                return None, "Please enter a valid quantity"
            
            try:
                custom_price = input("Sale price (press Enter for listed price): ").strip()
                sale_price = float(custom_price) if custom_price else None
                if sale_price and sale_price <= 0:
                    return None, "Sale price must be greater than 0"
            except ValueError:
                return None, "Please enter a valid price"
            
            return {
                'product_sku': product_sku,
                'quantity': quantity,
                'sale_price': sale_price
            }, None
            
        except KeyboardInterrupt:
            return None, "Input cancelled"
    
    @staticmethod
    def press_enter_to_continue():
        """Wait for user to press Enter"""
        input("\nPress Enter to continue...")