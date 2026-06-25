import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Business Intelligence Dashboard")

# 2. Gatekeeper Security Check
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔒 Access Denied. Please navigate to the **login** page and log in first.")
    st.stop()

# 3. Database connection helper
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=int(st.secrets["mysql"]["port"])
    )

# 4. Main Analytics Dashboard Logic
try:
    conn = get_db_connection()
    
    # Fetch KPI metrics via aggregate SQL queries
    kpi_df = pd.read_sql("SELECT SUM(revenue) as total_rev, COUNT(*) as total_sales, SUM(quantity) as total_qty FROM sales", conn)
    total_revenue = kpi_df['total_rev'].iloc[0] or 0.0
    total_sales_count = kpi_df['total_sales'].iloc[0] or 0
    total_units_sold = kpi_df['total_qty'].iloc[0] or 0

    # Display KPIs in clear visual metric columns
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("📦 Total Transactions", f"{total_sales_count}")
    col3.metric("📈 Total Units Sold", f"{total_units_sold}")
    
    st.markdown("---")
    
    # Grab data for interactive Plotly charts using SQL Group By
    chart_df = pd.read_sql("SELECT category, SUM(revenue) as revenue FROM sales GROUP BY category", conn)
    
    if not chart_df.empty:
        st.subheader("🛒 Category Revenue Breakdown (SQL Group By)")
        fig = px.bar(chart_df, x='category', y='revenue', color='category', text_auto='.2s')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Upload a CSV file in the 'Upload Data' tab to populate these metric visual charts.")
        
    conn.close()
except Exception as e:
    st.error(f"Error loading dashboard metrics: {e}")