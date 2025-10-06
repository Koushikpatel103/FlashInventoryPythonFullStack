from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ loads variables from .env file

class SupabaseDB:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        self.supabase: Client = create_client(url, key)

    # ---------------- PRODUCT METHODS ----------------

    def create_product(self, name, sku, price, stock_quantity):
        try:
            data = {
                "name": name,
                "sku": sku,
                "price": price,
                "stock_quantity": stock_quantity
            }
            response = self.supabase.table("products").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_products(self):
        try:
            response = self.supabase.table("products").select("*").execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_product_stock(self, product_id, new_stock):
        try:
            response = self.supabase.table("products").update({"stock_quantity": new_stock}).eq("id", product_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ---------------- SALES METHODS ----------------

    def create_sale(self, product_id, quantity, sale_price, sale_date=None):
        try:
            # Check product
            product_res = self.supabase.table("products").select("stock_quantity").eq("id", product_id).execute()
            if not product_res.data:
                return {"success": False, "error": "Product not found"}

            current_stock = product_res.data[0]["stock_quantity"]
            if current_stock < quantity:
                return {"success": False, "error": f"Not enough stock (Available: {current_stock})"}

            sale_data = {
                "product_id": product_id,
                "quantity_sold": quantity,  # ✅ match DB column
                "sale_price": sale_price
            }
            if sale_date:
                sale_data["sale_date"] = sale_date

            response = self.supabase.table("sales").insert(sale_data).execute()

            if response.data:
                # update stock
                new_stock = current_stock - quantity
                self.supabase.table("products").update({"stock_quantity": new_stock}).eq("id", product_id).execute()

            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_sales(self):
        try:
            response = self.supabase.table("sales").select("*, products(name, sku)").execute()
            sales = response.data
            for s in sales:
                s["quantity"] = s.get("quantity_sold", 0)
            return {"success": True, "data": sales}
        except Exception as e:
            return {"success": False, "error": str(e)}
