import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------- Configuration ----------------
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="📦 Flash Inventory System", layout="wide")

# ---------------- Helper Functions ----------------

def fetch_products():
    try:
        res = requests.get(f"{BACKEND_URL}/products/")
        data = res.json()
        return data.get("data", [])
    except Exception as e:
        st.error(f"Failed to fetch products: {e}")
        return []

def fetch_sales():
    try:
        res = requests.get(f"{BACKEND_URL}/sales/")
        data = res.json()
        if data.get("success"):
            return data.get("data", [])
        return []
    except Exception as e:
        st.error(f"Failed to fetch sales: {e}")
        return []

def record_sale(product_id, quantity, sale_price):
    try:
        res = requests.post(f"{BACKEND_URL}/sales/", json={
            "product_id": str(product_id),
            "quantity": quantity,
            "sale_price": sale_price
        })
        return res.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------------- Sidebar Navigation ----------------

st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add Product", "Update Products", "Record Sale", "View Sales"])

st.title("📦 Flash Inventory System")

# ---------------- Dashboard ----------------
if page == "Dashboard":
    st.header("📊 Inventory Overview")
    products = fetch_products()
    if products:
        df_products = pd.DataFrame(products)
        st.metric("Total Products", len(df_products))
        st.dataframe(df_products[["name", "sku", "price", "stock_quantity"]])
    else:
        st.info("No products found.")

# ---------------- Add Product ----------------
elif page == "Add Product":
    st.header("➕ Add New Product")
    with st.form("add_form"):
        name = st.text_input("Product Name")
        sku = st.text_input("SKU")
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        stock = st.number_input("Stock Quantity", min_value=0)
        submitted = st.form_submit_button("Add Product")
        if submitted:
            res = requests.post(f"{BACKEND_URL}/products/", json={
                "name": name, "sku": sku, "price": price, "stock_quantity": stock
            })
            data = res.json()
            if data.get("success"):
                st.success("✅ Product added successfully!")
            else:
                st.error(f"❌ {data.get('error')}")

# ---------------- Update Product ----------------
elif page == "Update Products":
    st.header("🔄 Update Product Stock")
    products = fetch_products()
    if products:
        product = st.selectbox("Select Product", products, format_func=lambda x: f"{x['name']} (Stock: {x['stock_quantity']})")
        new_stock = st.number_input("New Stock Quantity", min_value=0)
        if st.button("Update Stock"):
            res = requests.put(f"{BACKEND_URL}/products/{product['id']}/stock", params={"new_stock": new_stock})
            data = res.json()
            if data.get("success"):
                st.success("✅ Stock updated successfully!")
            else:
                st.error(f"❌ {data.get('error')}")
    else:
        st.warning("No products found.")

# ---------------- Record Sale ----------------
elif page == "Record Sale":
    st.header("🧾 Record Sale")
    products = fetch_products()
    if products:
        product = st.selectbox("Select Product", products, format_func=lambda x: f"{x['name']} (Stock: {x['stock_quantity']})")
        quantity = st.number_input("Quantity", min_value=1)
        sale_price = st.number_input("Sale Price", min_value=0.0, format="%.2f")
        if st.button("Record Sale"):
            result = record_sale(product["id"], quantity, sale_price)
            if result.get("success"):
                st.success("✅ Sale recorded successfully!")
            elif result.get("error"):
                st.error(f"❌ {result['error']}")
            else:
                st.warning("⚠️ Unexpected response.")
    else:
        st.warning("No products available for sale.")

# ---------------- View Sales ----------------
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

        # Summary metrics
        st.subheader("Sales Summary")
        total_revenue = df_sales["Total"].sum()
        total_items = df_sales["Quantity"].sum()
        st.metric("Total Revenue (₹)", f"{total_revenue:,.2f}")
        st.metric("Total Items Sold", total_items)

        # Revenue over time
        st.subheader("Revenue Over Time")
        df_time = df_sales.groupby("Date")[["Total"]].sum().reset_index()
        fig_time = px.line(df_time, x="Date", y="Total", title="Revenue Over Time")
        st.plotly_chart(fig_time, use_container_width=True)

        # Top-selling products
        st.subheader("Top Selling Products")
        df_top = df_sales.groupby("Product")[["Total", "Quantity"]].sum().sort_values("Total", ascending=False).reset_index()
        fig_top = px.bar(df_top, x="Product", y="Total", title="Top Selling Products", color="Total")
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("No sales recorded yet.")
