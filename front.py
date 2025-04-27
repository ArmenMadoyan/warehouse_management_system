# streamlit_app.py

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Connection URL
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "postgres"
DB_PORT = "5432"
DB_NAME = "mydatabase"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
@st.cache_resource
def get_engine():
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"❌ Error connecting to the database: {e}")
        return None

engine = get_engine()
if not engine:
    st.stop()

# --- User Authentication Functions ---

# Authenticate user
def authenticate_user(username, password):
    with engine.connect() as conn:
        query = text("""
            SELECT * FROM app_user 
            WHERE username = :username AND password_hash = :password
        """)
        result = conn.execute(query, {"username": username, "password": password}).fetchone()
        return result

# Register user
def register_user(username, password, full_name, user_role):
    try:
        with engine.begin() as conn:
            query = text("""
                INSERT INTO app_user (username, password_hash, full_name, user_role)
                VALUES (:username, :password, :full_name, :user_role)
            """)
            conn.execute(query, {
                "username": username,
                "password": password,
                "full_name": full_name,
                "user_role": user_role
            })
        return True, "User registered successfully."
    except Exception as e:
        return False, str(e)

# Read table
def read_table(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, con=engine)
    return df

# Custom SQL query
def custom_query(sql_query):
    df = pd.read_sql_query(sql_query, con=engine)
    return df

# --- Session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Main app ---
def main():
    st.title("📦 Warehouse Management System")

    if not st.session_state.logged_in:
        st.subheader("🔐 Welcome! Please Log In or Register")

        option = st.radio(
            "Do you already have an account?",
            ("Yes, I want to log in", "No, I want to register")
        )

        if option == "Yes, I want to log in":
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login_submit = st.form_submit_button("Login")
                if login_submit:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Login successful! 🎉")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        elif option == "No, I want to register":
            with st.form("register_form"):
                username = st.text_input("Create Username")
                password = st.text_input("Create Password", type="password")
                full_name = st.text_input("Full Name")
                user_role = st.selectbox("Select Role", ["admin", "manager", "staff"])
                register_submit = st.form_submit_button("Register")
                if register_submit:
                    success, msg = register_user(username, password, full_name, user_role)
                    if success:
                        st.success(msg + " Please log in now.")
                    else:
                        st.error(msg)

    else:
        st.sidebar.success(f"Logged in as {st.session_state.username}")

        pages = [
            "View Tables",
            "Low Stock Alerts",
            "Top Selling Products",
            "Revenue Reports",
            "Client Purchase History",
            "Logout"
        ]
        choice = st.sidebar.selectbox("Choose functionality:", pages)

        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

        if choice == "View Tables":
            st.header("📋 Browse Tables")
            tables = [
                "product", "warehouse", "inventory", "app_user", "client",
                "store", "purchase_order", "purchase_item", "sale_order", "sale_item", "payment"
            ]
            selected_table = st.selectbox("Select a table:", tables)
            df = read_table(selected_table)
            st.dataframe(df)

        elif choice == "Low Stock Alerts":
            st.header("🚨 Low Stock Alerts")
            query = """
                SELECT i.warehouse_id, w.warehouse_name, i.product_id, p.product_name, 
                       i.quantity_on_hand, i.reorder_level
                FROM inventory i
                JOIN warehouse w ON i.warehouse_id = w.warehouse_id
                JOIN product p ON i.product_id = p.product_id
                WHERE i.quantity_on_hand < i.reorder_level;
            """
            df = custom_query(query)
            if df.empty:
                st.info("No low stock items.")
            else:
                st.dataframe(df)

        elif choice == "Top Selling Products":
            st.header("🏆 Top Selling Products")
            top_n = st.slider("Select Top N Products:", 1, 20, 5)
            query = f"""
                SELECT p.product_name, SUM(si.quantity) AS total_units_sold
                FROM sale_item si
                JOIN product p ON si.product_id = p.product_id
                GROUP BY p.product_name
                ORDER BY total_units_sold DESC
                LIMIT {top_n};
            """
            df = custom_query(query)
            st.dataframe(df)
            st.bar_chart(df.set_index("product_name")["total_units_sold"])

        elif choice == "Revenue Reports":
            st.header("💰 Revenue Reports")
            report_type = st.selectbox("Choose report type:", ["Product Revenue", "Store Revenue", "Monthly Revenue"])

            if report_type == "Product Revenue":
                query = """
                    SELECT p.product_name, SUM(si.quantity * si.sale_price) AS revenue
                    FROM sale_item si
                    JOIN product p ON si.product_id = p.product_id
                    GROUP BY p.product_name;
                """
                df = custom_query(query)
                st.dataframe(df)
                st.bar_chart(df.set_index("product_name")["revenue"])

            elif report_type == "Store Revenue":
                query = """
                    SELECT s.store_name, SUM(si.quantity * si.sale_price) AS revenue
                    FROM sale_item si
                    JOIN sale_order so ON si.sale_id = so.sale_id
                    JOIN store s ON so.store_id = s.store_id
                    GROUP BY s.store_name;
                """
                df = custom_query(query)
                st.dataframe(df)
                st.bar_chart(df.set_index("store_name")["revenue"])

            elif report_type == "Monthly Revenue":
                query = """
                    SELECT DATE_TRUNC('month', so.sale_date) AS month, 
                           SUM(so.total_amount) AS revenue
                    FROM sale_order so
                    GROUP BY month
                    ORDER BY month;
                """
                df = custom_query(query)
                df['month'] = df['month'].dt.strftime('%Y-%m')
                st.dataframe(df)
                st.line_chart(df.set_index("month")["revenue"])

        elif choice == "Client Purchase History":
            st.header("🛒 Client Purchase History")
            clients = read_table("client")
            client_options = dict(zip(clients["client_id"], clients["client_name"]))
            selected_client_id = st.selectbox("Select Client:", options=list(client_options.keys()),
                                              format_func=lambda x: client_options[x])

            query = f"""
                SELECT so.sale_date, p.product_name, si.quantity, si.sale_price
                FROM sale_order so
                JOIN sale_item si ON so.sale_id = si.sale_id
                JOIN product p ON si.product_id = p.product_id
                WHERE so.client_id = {selected_client_id}
                ORDER BY so.sale_date;
            """
            df = custom_query(query)
            st.dataframe(df)


if __name__ == "__main__":
    main()
