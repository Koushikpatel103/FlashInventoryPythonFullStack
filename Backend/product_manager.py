from database import Database

class ProductManager:
    """
    Manages all product-related operations
    """
    
    def __init__(self):
        self.db = Database()
    
    def add_product(self, name, price, sku, initial_stock=0, category="General", description=""):
        """Add a new product to inventory"""
        # Validate input
        if not name or not sku:
            return None, "Product name and SKU are required!"
        
        if price <= 0:
            return None, "Price must be greater than 0!"
        
        if initial_stock < 0:
            return None, "Stock quantity cannot be negative!"
        
        # Check if SKU already exists
        existing_product, error = self.db.get_product_by_sku(sku)
        if error:
            return None, error
        if existing_product:
            return None, f"SKU '{sku}' already exists!"
        
        # Prepare product data
        product_data = {
            "name": name,
            "description": description,
            "sku": sku,
            "price": float(price),
            "stock_quantity": int(initial_stock),
            "min_stock_level": 5,
            "category": category
        }
        
        # Insert into database
        result, error = self.db.insert_product(product_data)
        if error:
            return None, error
        
        return result[0] if result else None, None
    
    def get_all_products(self):
        """Get all products"""
        products, error = self.db.get_all_products()
        if error:
            return [], error
        return products, None
    
    def get_product_by_sku(self, sku):
        """Get product by SKU"""
        return self.db.get_product_by_sku(sku)
    
    def search_products(self, search_term):
        """Search products by name or SKU"""
        products, error = self.db.get_all_products()
        if error:
            return [], error
        
        if not search_term:
            return products, None
        
        matching_products = []
        for product in products:
            if (search_term.lower() in product['name'].lower() or 
                search_term.lower() in product['sku'].lower()):
                matching_products.append(product)
        
        return matching_products, None
    
    def get_low_stock_products(self):
        """Get products with low stock"""
        products, error = self.db.get_all_products()
        if error:
            return [], error
        
        low_stock = [p for p in products if p['stock_quantity'] < p['min_stock_level']]
        return low_stock, None
    
    def update_stock(self, product_id, new_stock):
        """Update product stock level"""
        if new_stock < 0:
            return None, "Stock cannot be negative!"
        
        result, error = self.db.update_product_stock(product_id, new_stock)
        if error:
            return None, error
        
        return result, None