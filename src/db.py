import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")

supabase=create_client(url,key)

def create_product(name, sku, price, stock_quantity, category=None):
    response = supabase.table("products").insert({
            "name": name,
            "sku": sku,
            "price": price,
            "stock_quantity": stock_quantity,
            "category": category
        }).execute()
    return response.data, None

def get_all_products():
    return supabase.table("products").select("*").order("name").execute()

def get_product_id(product_id):
    return supabase.table("products").select("*").eq("id",product_id).execute()

def create_sale(product_id, quantity ,sale_price,sale_date=None):
    response=supabase.table("sales").insert({
        "product_id":product_id,
        "quantity":quantity,
        "sale_price":sale_price
    }).execute()
    return response.data,None

def get_sales():
    response=supabase.table("sales").select("*,products(name,sku)").order("sale_date",desc=True).execute()
    return response.data,None

