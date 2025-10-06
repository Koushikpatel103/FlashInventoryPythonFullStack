import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- CONFIG ----------------
API_BASE_URL = "http://localhost:8000"
st.set_page_config(page_title="📦 Flash Inventory System", layout="wide")

# ---------------- HELPER FUNCTIONS ----------------
def fetch_products():
    try:
        res = requests.get(f"{API_BASE_URL}/products")
        data = res.json()
        return data.get("data", []) if data.get("success") else []
    except:
        return []

def fetch_sales():
    try:
        res = requests.get(f"{API_BASE_URL}/sales")
        data = res.json()
        return data.get("data", []) if data.get("success") else []
    except:
        return []

def add_product(product_data):
    try:
        res = requests.post(f"{API_BASE_URL}/products", json=product_data)
        return res.json()
    except:
        return {"success": False, "error": "API connection failed"}

def update_product(product_id, update_data):
    try:
        res = requests.put(f"{API_BASE_URL}/products/{product_id}", json=update_data)
        return res.json()
    except:
        return {"success": False, "error": "API connection failed"}

def delete_product(product_id):
    try:
        res = requests.delete(f"{API_BASE_URL}/products/{product_id}")
        return res.json()
    except:
        return {"success": False, "error": "API connection failed"}

def record_sale(sale_data):
    try:
        res = requests.post(f"{API_BASE_URL}/sales", json=sale_data)
        return res.json()
    except:
        return {"success": False, "error": "API connection failed"}

# ---------------- NAVIGATION ----------------
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add Product", "Update Products", "Record Sale", "View Sales"])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.header("📊 Inventory Dashboard")
    
    products = fetch_products()
    sales = fetch_sales()

    total_products = len(products)
    total_stock_value = sum(p.get('price', 0) * p.get('stock_quantity', 0) for p in products)
    total_sales = len(sales)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products", total_products)
    col2.metric("Inventory Value (₹)", f"{total_stock_value:,.2f}")
    col3.metric("Total Sales", total_sales)

    st.subheader("Inventory by Category")
    if products:
        df_products = pd.DataFrame(products)
        fig = px.pie(df_products, names="category", values="stock_quantity", title="Stock Distribution by Category")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No products found")

# ---------------- ADD PRODUCT ----------------
elif page == "Add Product":
    st.header("➕ Add New Product")
    with st.form("add_product"):
        name = st.text_input("Product Name")
        sku = st.text_input("SKU")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)
        category = st.text_input("Category", value="General")
        description = st.text_area("Description", value="No description")
        submitted = st.form_submit_button("Add Product")
        
        if submitted:
            if name and sku:
                result = add_product({
                    "name": name,
                    "sku": sku,
                    "price": price,
                    "stock_quantity": stock_quantity,
                    "category": category,
                    "description": description
                })
                if result.get("success"):
                    st.success("✅ Product added successfully!")
                else:
                    st.error(f"❌ {result.get('error')}")
            else:
                st.error("Name and SKU are required")

# ---------------- UPDATE PRODUCTS ----------------
elif page == "Update Products":
    st.header("🔄 Update Products")
    products = fetch_products()
    if products:
        for product in products:
            with st.expander(f"{product['name']} (ID: {product['id']})"):
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Name", value=product['name'], key=f"name_{product['id']}")
                    new_price = st.number_input("Price", value=float(product['price']), key=f"price_{product['id']}")
                with col2:
                    new_stock = st.number_input("Stock", value=product['stock_quantity'], key=f"stock_{product['id']}")
                    new_category = st.text_input("Category", value=product.get('category', ''), key=f"cat_{product['id']}")
                
                if st.button("Update", key=f"update_{product['id']}"):
                    update_data = {
                        "name": new_name,
                        "price": new_price,
                        "stock_quantity": new_stock,
                        "category": new_category
                    }
                    result = update_product(product['id'], update_data)
                    if result.get("success"):
                        st.success("✅ Product updated successfully!")
                    else:
                        st.error(f"❌ {result.get('error')}")
                
                if st.button("Delete", key=f"delete_{product['id']}"):
                    result = delete_product(product['id'])
                    if result.get("success"):
                        st.success("✅ Product deleted!")
                        st.experimental_rerun()
                    else:
                        st.error(f"❌ {result.get('error')}")
    else:
        st.info("No products found")

# ---------------- RECORD SALE ----------------
elif page == "Record Sale":
    st.header("🧾 Record Sale")
    products = fetch_products()
    if products:
        available_products = [p for p in products if p['stock_quantity'] > 0]
        if available_products:
            product_options = {f"{p['name']} (Stock: {p['stock_quantity']})": p['id'] for p in available_products}
            with st.form("record_sale"):
                selected = st.selectbox("Select Product", list(product_options.keys()))
                quantity = st.number_input("Quantity", min_value=1, value=1)
                sale_price = st.number_input("Sale Price", min_value=0.0, step=0.01)
                if st.form_submit_button("Record Sale"):
                    product_id = product_options[selected]
                    result = record_sale({
                        "product_id": product_id,
                        "quantity": quantity,
                        "sale_price": sale_price
                    })
                    if result.get("success"):
                        st.success("✅ Sale recorded successfully!")
                    else:
                        st.error(f"❌ {result.get('error')}")
        else:
            st.warning("No products available for sale")
    else:
        st.warning("No products found")

# ---------------- VIEW SALES ----------------
elif page == "View Sales":
    st.header("📄 Sales History")
    sales = fetch_sales()
    if sales:
        sales_list = []
        for sale in sales:
            product_name = sale.get('products', {}).get('name', 'Unknown')
            quantity = sale.get('quantity', 0)
            price = sale.get('sale_price', 0)
            date = sale.get('sale_date', '')
            sales_list.append({
                "Product": product_name,
                "Quantity": quantity,
                "Price": price,
                "Total": quantity * price,
                "Date": pd.to_datetime(date)
            })
        df_sales = pd.DataFrame(sales_list)
        st.dataframe(df_sales.sort_values("Date", ascending=False))

        st.subheader("Sales Summary")
        total_revenue = df_sales["Total"].sum()
        total_items = df_sales["Quantity"].sum()
        st.metric("Total Revenue (₹)", f"{total_revenue:,.2f}")
        st.metric("Total Items Sold", total_items)

        st.subheader("Sales Over Time")
        fig_time = px.line(df_sales.groupby("Date").sum().reset_index(), x="Date", y="Total", title="Revenue Over Time")
        st.plotly_chart(fig_time, use_container_width=True)

        st.subheader("Top Selling Products")
        top_products = df_sales.groupby("Product").sum().sort_values("Total", ascending=False).reset_index()
        fig_top = px.bar(top_products, x="Product", y="Total", title="Top Selling Products", color="Total")
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("No sales recorded yet")
