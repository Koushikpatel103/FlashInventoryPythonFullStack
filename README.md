# E-commerce Inventory management System

FlashInventory is a simple yet powerful inventory management system that helps businesses track products, monitor stock levels, and manage sales data using a modern web-based database (Supabase).

## Project Goals:

>Track product information (name, price, SKU, stock levels)
Monitor low stock alerts

>Record sales transactions

>Provide easy-to-use menu interface

>Store data securely in the cloud

## Project Structure

FlashInventory
|
|---src/                # core application logic
    |----logic.py       # Business logic and task
operations
    |---db.py           #Database operations
|
|---api.py/             #Backend API
|   |__main.py          #FastApi
|
|----frontend/          #Frontend Application
|   |__app.py           #streamlit web interface
|
|___requirements.txt    #python Dependencies
|
|___README.md           #Project Documentation
|
|---.env                #Python Varaiables

### 1 clone or Download the project
# option 1: clone with git
git clone <repository-url>

# option 2: Download and Extract the zip file

### 2.Install all requirements python packages
pip install -r requirements.txt

### 3 set up supabase DataBase

1.create a supabase project:
2.create the tasks table
-go to the sql editor in your supabase dashboard

-- Products table
CREATE TABLE products (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    sku TEXT UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2),
    stock_quantity INTEGER DEFAULT 0,
    min_stock_level INTEGER DEFAULT 5,
    category TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sales table 
CREATE TABLE sales (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    product_id UUID REFERENCES products(id),
    quantity_sold INTEGER NOT NULL,
    sale_price DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT NOW()
);

# Get your credentials

### 4. Configure Environment Variables

1.create a '.env' file in the projects root

2.Add your supabase credentials to .env file
SUPABASE_URL="https://stytcwscjyvhpwhetdha.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0eXRjd3Njanl2aHB3aGV0ZGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIwNzMsImV4cCI6MjA3MzY1ODA3M30.XMBrZ4vJztg25LIc5o4u6jXFkxvYWUGJn8t2i6P3NI"

### 5. Run the application

## Streammlit Frontend
streamlit run frontend/app.py

# Frontend (Streamlit)

Runs on http://localhost:8501

Started with Streamlit command

Python web framework for the user interface

# Backend (FastAPI)

Runs on http://localhost:8000

Started by navigating to the api directory and running python main.py

Python REST API framework for backend operations

# Technology Stack

**Frontend**: Streamlit (Python web framework)

**Backend**: FastAPI (Python REST API framework)

**Database**: Supabase (PostgreSQL-based backend-as-a-service)

**Language**: Python 3.8+

### Key Components

.src/db.py: Database operations

Handles all CRUD operations with Supabase

.src/logic.py: Business logic

Task validation and processing

## Troubleshooting

# Common Issues

.Module not found" errors

Make sure you've installed all dependencies: pip install -r requirements.txt

Check that you're running commands from the correct directory

## Future Enhancements

Ideas for extending this project

# Features:
- Monthly sales trends and charts
- Best-selling products ranking
- Revenue forecasting
- Seasonal sales patterns
- Customer buying behavior analysis

# Track:
- Cost price vs sale price
- Gross profit per product
- Net profit calculations
- Most profitable categories
- Return on investment (ROI)

# Support 

If you encounter any issues or have questions:

**phone**:6309248221
**Email**:koushikpatel103@gmail.com









