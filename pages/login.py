import streamlit as st
import mysql.connector

st.set_page_config(page_title="User Authentication", page_icon="🔑")
st.title("🔑 Platform Login")

def get_db_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=int(st.secrets["mysql"]["port"])
    )

# Initialize login session state variable if it doesn't exist
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# If user is already logged in, show a logout choice
if st.session_state["logged_in"]:
    st.success(f"Welcome back, {st.session_state['username']}!")
    if st.button("🚪 Log Out"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()
else:
    # Login input form boxes
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    
    if st.button("🔐 Authenticate via SQL"):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Pure SQL lookup query checking users table
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username_input, password_input))
            user_record = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user_record:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username_input
                st.success("✅ Login successful! You now have full dashboard access.")
                st.rerun()
            else:
                st.error("❌ Invalid Username or Password. Try again.")
                
        except Exception as e:
            st.error(f"Authentication Error: {e}")
            
    st.info("💡 Default system access for assignment testing:\n* **Username:** `admin` \n* **Password:** `admin123`")