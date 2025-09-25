from database import Database
from datetime import datetime, timedelta

class SalesManager:
    """Manages sales-related operations"""
    
    def __init__(self):
        self.db = Database()
    
    def record_sale(self, product_id, quantity_sold, sale_price=None):
        """Record a new sale"""
        # Validate input
        if quantity_sold <= 0:
            return None, "Quantity must be greater than 0"
        
        # Prepare sale data
        sale_data = {
            "product_id": product_id,
            "quantity_sold": quantity_sold,
            "sale_price": float(sale_price) if sale_price else None
        }
        
        # Record sale
        result, error = self.db.insert_sale(sale_data)
        if error:
            return None, error
        
        return result[0] if result else None, None
    
    def get_all_sales(self):
        """Get all sales"""
        return self.db.get_all_sales()
    
    def get_recent_sales(self, limit=10):
        """Get recent sales"""
        return self.db.get_recent_sales(limit)
    
    def get_sales_report(self, days=30):
        """Generate sales report for specified period"""
        all_sales, error = self.db.get_all_sales()
        if error:
            return {}, error
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter recent sales
        recent_sales = []
        for sale in all_sales:
            sale_date = datetime.fromisoformat(sale['sale_date'].replace('Z', '+00:00'))
            if sale_date > cutoff_date:
                recent_sales.append(sale)
        
        # Calculate metrics
        total_revenue = sum(sale['sale_price'] * sale['quantity_sold'] for sale in recent_sales)
        total_items_sold = sum(sale['quantity_sold'] for sale in recent_sales)
        
        report = {
            "period_days": days,
            "total_sales": len(recent_sales),
            "total_revenue": total_revenue,
            "total_items_sold": total_items_sold,
            "average_sale_value": total_revenue / len(recent_sales) if recent_sales else 0
        }
        
        return report, None