import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

class Database:
    """
    Handles all database operations - the connection layer to Supabase
    """
    
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        print("🔌 Database connection initialized!")
    
    def test_connection(self):
        """Test database connection"""
        try:
            response = self.supabase.table('products').select('*').limit(1).execute()
            return True, "✅ Database connection successful!"
        except Exception as e:
            return False, f"❌ Database connection failed: {e}"
    
    # PRODUCTS TABLE OPERATIONS
    def insert_product(self, product_data):
        """Insert a new product"""
        try:
            response = self.supabase.table('products').insert(product_data).execute()
            return response.data, None
        except Exception as e:
            return None, f"Error inserting product: {e}"
    
    def get_all_products(self):
        """Get all products"""
        try:
            response = self.supabase.table('products').select('*').order('name').execute()
            return response.data, None
        except Exception as e:
            return None, f"Error fetching products: {e}"
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        try:
            response = self.supabase.table('products').select('*').eq('id', product_id).execute()
            return response.data[0] if response.data else None, None
        except Exception as e:
            return None, f"Error fetching product: {e}"
    
    def get_product_by_sku(self, sku):
        """Get product by SKU"""
        try:
            response = self.supabase.table('products').select('*').eq('sku', sku).execute()
            return response.data[0] if response.data else None, None
        except Exception as e:
            return None, f"Error fetching product by SKU: {e}"
    
    def update_product_stock(self, product_id, new_stock):
        """Update product stock quantity"""
        try:
            response = self.supabase.table('products').update({'stock_quantity': new_stock}).eq('id', product_id).execute()
            return response.data, None
        except Exception as e:
            return None, f"Error updating stock: {e}"
    
    # SALES TABLE OPERATIONS
    def insert_sale(self, sale_data):
        """Record a new sale"""
        try:
            response = self.supabase.table('sales').insert(sale_data).execute()
            return response.data, None
        except Exception as e:
            return None, f"Error recording sale: {e}"
    
    def get_all_sales(self):
        """Get all sales with product information"""
        try:
            response = self.supabase.table('sales').select('*, products(name, sku)').order('sale_date', desc=True).execute()
            return response.data, None
        except Exception as e:
            return None, f"Error fetching sales: {e}"
    
    def get_sales_by_product(self, product_id):
        """Get sales for a specific product"""
        try:
            response = self.supabase.table('sales').select('*').eq('product_id', product_id).execute()
            return response.data, None
        except Exception as e:
            return None, f"Error fetching product sales: {e}"
    
    def get_recent_sales(self, limit=10):
        """Get recent sales"""
        try:
            response = self.supabase.table('sales').select('*, products(name, sku)').order('sale_date', desc=True).limit(limit).execute()
            return response.data, None
        except Exception as e:
            return None, f"Error fetching recent sales: {e}"