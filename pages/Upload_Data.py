import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(page_title="Upload Data", page_icon="📤")
st.title("📤 Operational Data Upload")

# Database connection helper
def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=int(st.secrets["mysql"]["port"])
    )

uploaded_file = st.file_uploader("Choose your 100-entry Retail Sales CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📋 **Preview of uploaded data:**", df.head())
    
    if st.button("🚀 Push Data to MySQL Database"):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Clear previous records to avoid cluttering metrics
            cursor.execute("TRUNCATE TABLE sales")
            
            # Insert entries sequentially
            success_count = 0
            for index, row in df.iterrows():
                sql = """INSERT INTO sales (product_name, category, quantity, revenue, sale_date) 
                         VALUES (%s, %s, %s, %s, %s)"""
                values = (row['product_name'], row['category'], int(row['quantity']), float(row['revenue']), row['sale_date'])
                cursor.execute(sql, values)
                success_count += 1
                
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"✅ Successfully inserted {success_count} records into your Railway SQL Database!")
        except Exception as e:
            st.error(f"❌ Error inserting data: {e}")