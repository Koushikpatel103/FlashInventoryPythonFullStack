from src.db import DatabaseManager

class FlashInventory:
    def __init__(self):
        self.db = DatabaseManager()

    def add_product(self, name, sku, price, stock_quantity, category=None, description=None):
        if not name or not sku:
            return {"success": False, "error": "Name and SKU are required"}
        if price <= 0:
            return {"success": False, "error": "Price must be > 0"}
        if stock_quantity < 0:
            return {"success": False, "error": "Invalid stock"}
        return self.db.create_product(name, sku, price, stock_quantity, category, description)

    def get_products(self):
        return self.db.get_all_products()

    def get_product_by_id(self, pid):
        return self.db.get_product_by_id(pid)

    def update_product(self, pid, **kwargs):
        if not kwargs:
            return {"success": False, "error": "No data to update"}
        return self.db.update_product(pid, **kwargs)

    def delete_product(self, pid):
        return self.db.delete_product(pid)

    def record_sale(self, product_id, quantity, sale_price, sale_date=None):
        if quantity <= 0:
            return {"success": False, "error": "Quantity must be > 0"}
        if sale_price <= 0:
            return {"success": False, "error": "Sale price must be > 0"}
        return self.db.create_sale(product_id, quantity, sale_price, sale_date)

    def get_sales(self):
        return self.db.get_sales()
