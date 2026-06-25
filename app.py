import streamlit as st
import mysql.connector

# Set up page config
st.set_page_config(page_title="RetailIQ Analytics Platform", page_icon="📈", layout="wide")

# Database Connection Function using Streamlit Secrets
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=int(st.secrets["mysql"]["port"])
    )

# Automatically initialize tables in the cloud
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(100),
            role VARCHAR(50)
        )""")
        
        # 2. Sales Data Table (Compulsory SQL Business Database)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100),
            category VARCHAR(100),
            quantity INT,
            revenue DECIMAL(10,2),
            sale_date DATE
        )""")
        
        # Seed a default admin user if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'Admin')")
            
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return False

# Run database setup behind the scenes
tables_ready = init_db()

# Main Landing Page UI
st.title("📈 RetailIQ Operational Analytics Platform")
st.markdown("---")

if tables_ready:
    st.success("✅ Connected securely to Railway MySQL Cloud Database.")
    st.info("👈 Use the sidebar navigation menu to **Upload Data** or view your **Dashboard** metrics.")
else:
    st.warning("⚠️ Waiting for active database link setup parameters.")