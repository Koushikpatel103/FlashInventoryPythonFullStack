from fastapi import FastAPI
from pydantic import BaseModel
from src.db import SupabaseDB
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI(title="Flash Inventory System API")
db = SupabaseDB()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Pydantic Models ----------------

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    stock_quantity: int

class SaleCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int
    sale_price: float

# ---------------- Routes ----------------

@app.get("/")
def root():
    return {"message": "Flash Inventory API is running"}

@app.post("/products/")
def add_product(product: ProductCreate):
    return db.create_product(product.name, product.sku, product.price, product.stock_quantity)

@app.get("/products/")
def list_products():
    return db.get_products()

@app.put("/products/{product_id}/stock")
def update_stock(product_id: uuid.UUID, new_stock: int):
    return db.update_product_stock(product_id, new_stock)

@app.post("/sales/")
def record_sale(sale: SaleCreate):
    return db.create_sale(str(sale.product_id), sale.quantity, sale.sale_price)

@app.get("/sales/")
def list_sales():
    return db.get_sales()
