import mysql.connector

conn = mysql.connector.connect(
    host="reseau.proxy.rlwy.net",
    user="root",
    password="wKyfYtfPrhYlLKRTciMczrVNICEmXGsI",
    database="railway",
    port=20056
)

cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100),
    role VARCHAR(50)
)
""")

# Login history
cursor.execute("""
CREATE TABLE IF NOT EXISTS login_history(
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    login_time DATETIME,
    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
)
""")

# Upload history
cursor.execute("""
CREATE TABLE IF NOT EXISTS upload_history(
    upload_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    file_name VARCHAR(255),
    upload_time DATETIME,
    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
)
""")

# Sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
    quantity INT,
    revenue DECIMAL(10,2),
    sale_date DATE
)
""")

conn.commit()

print("All tables created successfully!")