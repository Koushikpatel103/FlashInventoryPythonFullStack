from database import Database
from datetime import datetime, timedelta

class SalesManager:
    """
    Manages all sales-related operations
    """
    
    def __init__(self):
        self.db = Database()
    
    def record_sale(self, product_id, quantity_sold, sale_price=None):
        """Record a new sale"""
        # Get product current price if sale_price not provided
        if sale_price is None:
            product, error = self.db.get_product_by_id(product_id)
            if error or not product:
                return None, "Product not found!"
            sale_price = product['price']
        
        # Validate sale data
        if quantity_sold <= 0:
            return None, "Quantity must be greater than 0!"
        
        if sale_price <= 0:
            return None, "Sale price must be greater than 0!"
        
        # Prepare sale data
        sale_data = {
            "product_id": product_id,
            "quantity_sold": quantity_sold,
            "sale_price": float(sale_price)
            # sale_date is automatically set by database
        }
        
        # Record sale
        result, error = self.db.insert_sale(sale_data)
        if error:
            return None, error
        
        return result[0] if result else None, None
    
    def get_all_sales(self):
        """Get all sales with product details"""
        sales, error = self.db.get_all_sales()
        if error:
            return [], error
        return sales, None
    
    def get_recent_sales(self, limit=10):
        """Get recent sales"""
        sales, error = self.db.get_recent_sales(limit)
        if error:
            return [], error
        return sales, None
    
    def get_sales_by_product(self, product_id):
        """Get sales for a specific product"""
        sales, error = self.db.get_sales_by_product(product_id)
        if error:
            return [], error
        return sales, None
    
    def get_sales_report(self, days=30):
        """Generate sales report for specified period"""
        all_sales, error = self.db.get_all_sales()
        if error:
            return {}, error
        
        # Filter sales by date
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sales = [
            sale for sale in all_sales 
            if datetime.fromisoformat(sale['sale_date'].replace('Z', '+00:00')) > cutoff_date
        ]
        
        if not recent_sales:
            return {
                "period_days": days,
                "total_sales": 0,
                "total_revenue": 0,
                "total_items_sold": 0,
                "average_sale_value": 0
            }, None
        
        # Calculate metrics
        total_revenue = sum(sale['sale_price'] * sale['quantity_sold'] for sale in recent_sales)
        total_items_sold = sum(sale['quantity_sold'] for sale in recent_sales)
        
        report = {
            "period_days": days,
            "total_sales": len(recent_sales),
            "total_revenue": total_revenue,
            "total_items_sold": total_items_sold,
            "average_sale_value": total_revenue / len(recent_sales) if recent_sales else 0,
            "start_date": cutoff_date.strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        return report, None
    
    def get_daily_sales(self, days=7):
        """Get daily sales breakdown"""
        all_sales, error = self.db.get_all_sales()
        if error:
            return [], error
        
        # Group sales by date
        daily_sales = {}
        for sale in all_sales:
            sale_date = sale['sale_date'][:10]  # Extract YYYY-MM-DD
            
            if sale_date not in daily_sales:
                daily_sales[sale_date] = {
                    'date': sale_date,
                    'total_sales': 0,
                    'total_revenue': 0,
                    'items_sold': 0
                }
            
            daily_sales[sale_date]['total_sales'] += 1
            daily_sales[sale_date]['total_revenue'] += sale['sale_price'] * sale['quantity_sold']
            daily_sales[sale_date]['items_sold'] += sale['quantity_sold']
        
        # Convert to list and sort by date
        daily_list = sorted(daily_sales.values(), key=lambda x: x['date'], reverse=True)
        
        # Return only requested number of days
        return daily_list[:days], None