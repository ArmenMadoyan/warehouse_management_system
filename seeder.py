# seed_database.py
import psycopg2
import time

POSTGRES_USER = "myuser"
POSTGRES_PASSWORD = "mypassword"
POSTGRES_HOST = "postgres"
POSTGRES_PORT = "5432"
TARGET_DATABASE = "mydatabase"

# Connect to default 'postgres' DB
def get_server_connection():
    return psycopg2.connect(
        dbname="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )

# Connect to target WMS database
def get_db_connection():
    return psycopg2.connect(
        dbname=TARGET_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )

# Create database if not exists
def create_database():
    conn = get_server_connection()
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TARGET_DATABASE}'")
    exists = cursor.fetchone()
    if not exists:
        print(f"📦 Creating database {TARGET_DATABASE}...")
        cursor.execute(f"CREATE DATABASE {TARGET_DATABASE};")
    else:
        print(f"✅ Database {TARGET_DATABASE} already exists.")
    cursor.close()
    conn.close()

# Create tables according to DDL
def create_tables():
    ddl_statements = """
    CREATE TABLE IF NOT EXISTS product (
      product_id   SERIAL PRIMARY KEY,
      product_name VARCHAR(100) NOT NULL,
      description  TEXT,
      weight       DECIMAL(8,2) NOT NULL CHECK (weight >= 0),
      unit_cost    DECIMAL(10,2) NOT NULL CHECK (unit_cost >= 0),
      unit_price   DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0)
    );

    CREATE TABLE IF NOT EXISTS warehouse (
      warehouse_id SERIAL PRIMARY KEY,
      warehouse_name VARCHAR(100) NOT NULL,
      warehouse_location VARCHAR(200)
    );

    CREATE TABLE IF NOT EXISTS inventory (
      warehouse_id INT NOT NULL,
      product_id INT NOT NULL,
      quantity_on_hand INT DEFAULT 0 CHECK (quantity_on_hand >= 0),
      reorder_level INT DEFAULT 0 CHECK (reorder_level >= 0),
      PRIMARY KEY (warehouse_id, product_id),
      FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id),
      FOREIGN KEY (product_id) REFERENCES product(product_id)
    );

    CREATE TABLE IF NOT EXISTS app_user (
      user_id SERIAL PRIMARY KEY,
      username VARCHAR(50) NOT NULL UNIQUE,
      password_hash VARCHAR(255) NOT NULL,
      full_name VARCHAR(100) NOT NULL,
      user_role VARCHAR(50) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS client (
      client_id SERIAL PRIMARY KEY,
      client_name VARCHAR(100) NOT NULL,
      email VARCHAR(100),
      phone VARCHAR(20)
    );

    CREATE TABLE IF NOT EXISTS store (
      store_id SERIAL PRIMARY KEY,
      store_name VARCHAR(100) NOT NULL,
      store_location VARCHAR(200)
    );

    CREATE TABLE IF NOT EXISTS purchase_order (
      purchase_id SERIAL PRIMARY KEY,
      purchase_date DATE NOT NULL,
      total_cost DECIMAL(12,2) NOT NULL CHECK (total_cost >= 0),
      warehouse_id INT NOT NULL,
      user_id INT NOT NULL,
      FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id),
      FOREIGN KEY (user_id) REFERENCES app_user(user_id)
    );

    CREATE TABLE IF NOT EXISTS purchase_item (
      purchase_id INT NOT NULL,
      product_id INT NOT NULL,
      unit_cost DECIMAL(10,2) NOT NULL CHECK (unit_cost >= 0),
      quantity INT NOT NULL CHECK (quantity > 0),
      PRIMARY KEY (purchase_id, product_id),
      FOREIGN KEY (purchase_id) REFERENCES purchase_order(purchase_id),
      FOREIGN KEY (product_id) REFERENCES product(product_id)
    );

    CREATE TABLE IF NOT EXISTS sale_order (
      sale_id SERIAL PRIMARY KEY,
      sale_date DATE NOT NULL,
      total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),
      client_id INT NOT NULL,
      store_id INT NOT NULL,
      user_id INT NOT NULL,
      FOREIGN KEY (client_id) REFERENCES client(client_id),
      FOREIGN KEY (store_id) REFERENCES store(store_id),
      FOREIGN KEY (user_id) REFERENCES app_user(user_id)
    );

    CREATE TABLE IF NOT EXISTS sale_item (
      sale_id INT NOT NULL,
      product_id INT NOT NULL,
      sale_price DECIMAL(10,2) NOT NULL CHECK (sale_price >= 0),
      quantity INT NOT NULL CHECK (quantity > 0),
      PRIMARY KEY (sale_id, product_id),
      FOREIGN KEY (sale_id) REFERENCES sale_order(sale_id),
      FOREIGN KEY (product_id) REFERENCES product(product_id)
    );

    CREATE TABLE IF NOT EXISTS payment (
      payment_id SERIAL PRIMARY KEY,
      payment_date DATE NOT NULL,
      amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
      payment_method VARCHAR(50),
      reference_number VARCHAR(100),
      sale_id INT NOT NULL UNIQUE,
      FOREIGN KEY (sale_id) REFERENCES sale_order(sale_id)
    );
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(ddl_statements)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables created successfully.")
# Seed initial data
def seed_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ==================== PRODUCTS ====================
        cursor.execute(
            "TRUNCATE TABLE payment, sale_item, sale_order, purchase_item, purchase_order, inventory, store, client, app_user, warehouse, product CASCADE;")

        cursor.execute("""
        INSERT INTO product (product_id, product_name, description, weight, unit_cost, unit_price) VALUES
        (1, 'Product 1', 'Description for product 1', 6.39, 13.44, 137.97),
        (2, 'Product 2', 'Description for product 2', 8.91, 44.42, 106.02),
        (3, 'Product 3', 'Description for product 3', 8.98, 8.91, 97.97),
        (4, 'Product 4', 'Description for product 4', 1.50, 19.27, 79.76),
        (5, 'Product 5', 'Description for product 5', 8.01, 6.92, 84.37),
        (6, 'Product 6', 'Description for product 6', 7.15, 42.37, 75.21),
        (7, 'Product 7', 'Description for product 7', 7.30, 46.79, 113.45),
        (8, 'Product 8', 'Description for product 8', 5.46, 39.29, 103.40),
        (9, 'Product 9', 'Description for product 9', 9.33, 12.34, 120.58),
        (10, 'Product 10', 'Description for product 10', 2.09, 18.07, 145.96);
        """)

        # ==================== WAREHOUSES ====================
        cursor.execute("""
        INSERT INTO warehouse (warehouse_id, warehouse_name, warehouse_location) VALUES
        (1, 'Central Warehouse', 'Yerevan'),
        (2, 'North Warehouse', 'Gyumri'),
        (3, 'South Warehouse', 'Kapan');
        """)

        # ==================== INVENTORY ====================
        cursor.execute("""
        INSERT INTO inventory (warehouse_id, product_id, quantity_on_hand, reorder_level) VALUES
        -- Warehouse 1
        (1,1,181,33),(1,2,179,23),(1,3,113,30),(1,4,6,25),(1,5,51,44),
        (1,6,75,40),(1,7,54,39),(1,8,104,33),(1,9,2,43),(1,10,117,50),
        -- Warehouse 2
        (2,1,72,44),(2,2,121,20),(2,3,93,36),(2,4,195,21),(2,5,180,32),
        (2,6,10,47),(2,7,139,40),(2,8,27,23),(2,9,130,32),(2,10,191,23),
        -- Warehouse 3
        (3,1,13,30),(3,2,43,39),(3,3,88,45),(3,4,180,42),(3,5,106,28),
        (3,6,34,39),(3,7,0,41),(3,8,171,45),(3,9,44,44),(3,10,131,35);
        """)

        # ==================== USERS ====================
        cursor.execute("""
        INSERT INTO app_user (user_id, username, password_hash, full_name, user_role) VALUES
        (1, 'user1', 'md5hash', 'User 1', 'Accountant'),
        (2, 'user2', 'md5hash', 'User 2', 'Owner'),
        (3, 'user3', 'md5hash', 'User 3', 'Accountant'),
        (4, 'user4', 'md5hash', 'User 4', 'Accountant'),
        (5, 'user5', 'md5hash', 'User 5', 'Worker');
        """)

        # ==================== CLIENTS ====================
        cursor.execute("""
        INSERT INTO client (client_id, client_name, email, phone) VALUES
        (1, 'Client 1', 'client1@example.com', '+374 24818913'),
        (2, 'Client 2', 'client2@example.com', '+374 58276946'),
        (3, 'Client 3', 'client3@example.com', '+374 92554649'),
        (4, 'Client 4', 'client4@example.com', '+374 63630157'),
        (5, 'Client 5', 'client5@example.com', '+374 32468553'),
        (6, 'Client 6', 'client6@example.com', '+374 93668205'),
        (7, 'Client 7', 'client7@example.com', '+374 76575420'),
        (8, 'Client 8', 'client8@example.com', '+374 25796548'),
        (9, 'Client 9', 'client9@example.com', '+374 57914837'),
        (10, 'Client 10', 'client10@example.com', '+374 19914789');
        """)

        # ==================== STORES ====================
        cursor.execute("""
        INSERT INTO store (store_id, store_name, store_location) VALUES
        (1, 'Store A', 'Yerevan'),
        (2, 'Store B', 'Gyumri'),
        (3, 'Store C', 'Vanadzor');
        """)

        # ==================== PURCHASE ORDERS and ITEMS ====================
        # NOTE: First purchase_items must be inserted because of FK dependency
        cursor.execute("""
        INSERT INTO purchase_item (purchase_id, product_id, unit_cost, quantity) VALUES
        (1,1,13.44,16), (1,5,6.92,25), (1,4,19.27,20),
        (2,2,44.42,26), (2,8,39.29,16), (2,4,19.27,26),
        (3,6,42.37,24), (3,3,8.91,8), (3,5,6.92,28),
        (4,2,44.42,29), (4,10,18.07,20), (4,9,12.34,21),
        (5,7,46.79,14), (5,9,12.34,15), (5,4,19.27,24),
        (6,3,8.91,14), (6,8,39.29,12), (6,5,6.92,28),
        (7,9,12.34,23), (7,7,46.79,28), (7,6,42.37,17),
        (8,10,18.07,30), (8,4,19.27,6), (8,1,13.44,29),
        (9,2,44.42,22), (9,6,42.37,25), (9,5,6.92,30),
        (10,8,39.29,7), (10,3,8.91,28), (10,1,13.44,15),
        (11,7,46.79,29), (11,5,6.92,16), (11,9,12.34,20),
        (12,2,44.42,13), (12,6,42.37,17), (12,10,18.07,19),
        (13,4,19.27,25), (13,8,39.29,14), (13,7,46.79,14),
        (14,3,8.91,22), (14,6,42.37,25), (14,9,12.34,29),
        (15,1,13.44,13), (15,10,18.07,24), (15,5,6.92,28),
        (16,2,44.42,7), (16,7,46.79,29), (16,4,19.27,30);
        """)

        cursor.execute("""
        INSERT INTO purchase_order (purchase_id, purchase_date, total_cost, warehouse_id, user_id) VALUES
        (1,'2024-11-22',665.04,1,4),
        (2,'2024-05-06',2416.38,1,1),
        (3,'2024-11-24',1575.64,3,3),
        (4,'2025-01-03',2623.74,2,3),
        (5,'2024-10-01',1589.41,2,2),
        (6,'2024-03-15',1118.66,3,5),
        (7,'2025-01-19',2346.05,1,2),
        (8,'2024-09-20',1300.11,1,1),
        (9,'2024-07-08',2142.14,3,4),
        (10,'2025-04-03',1123.37,3,2),
        (11,'2024-12-15',2232.41,2,3),
        (12,'2025-01-07',1830.88,3,1),
        (13,'2024-06-29',2616.63,1,5),
        (14,'2024-08-12',2354.39,2,4),
        (15,'2024-03-16',2799.32,1,2),
        (16,'2024-03-16',2799.32,1,2);
        """)

        # ==================== SALES and PAYMENTS ====================
        cursor.execute("""
        INSERT INTO sale_order (sale_id, sale_date, total_amount, client_id, store_id, user_id) VALUES
        (1,'2025-01-10',360.31,1,1,2),
        (2,'2025-02-14',477.58,2,2,3),
        (3,'2025-03-03',248.39,3,3,4),
        (4,'2025-01-20',216.85,4,1,1),
        (5,'2025-02-25',387.12,5,2,5),
        (6,'2025-03-15',341.96,6,3,2),
        (7,'2025-04-05',239.28,7,1,3),
        (8,'2025-04-10',243.95,8,2,4),
        (9,'2025-04-12',330.30,9,3,5),
        (10,'2025-04-15',412.50,10,1,1);
        """)

        cursor.execute("""
        INSERT INTO sale_item (sale_id, product_id, sale_price, quantity) VALUES
        (1,1,137.97,2),(1,5,84.37,1),
        (2,2,106.02,3),(2,4,79.76,2),
        (3,3,97.97,1),(3,6,75.21,2),
        (4,7,113.45,1),(4,8,103.40,1),
        (5,9,120.58,2),(5,10,145.96,1),
        (6,1,137.97,1),(6,2,106.02,1),(6,3,97.97,1),
        (7,4,79.76,3),
        (8,5,84.37,2),(8,6,75.21,1),
        (9,7,113.45,2),(9,8,103.40,1),
        (10,9,120.58,1),(10,10,145.96,2);
        """)

        cursor.execute("""
        INSERT INTO payment (payment_id, payment_date, amount, payment_method, reference_number, sale_id) VALUES
        (1,'2025-01-11',360.31,'Cash','REF0001',1),
        (2,'2025-02-15',477.58,'Credit Card','REF0002',2),
        (3,'2025-03-04',248.39,'Bank Transfer','REF0003',3),
        (4,'2025-01-21',216.85,'Cash','REF0004',4),
        (5,'2025-02-26',387.12,'Credit Card','REF0005',5),
        (6,'2025-03-16',341.96,'Bank Transfer','REF0006',6),
        (7,'2025-04-06',239.28,'Cash','REF0007',7),
        (8,'2025-04-11',243.95,'Credit Card','REF0008',8),
        (9,'2025-04-13',330.30,'Bank Transfer','REF0009',9),
        (10,'2025-04-16',412.50,'Cash','REF0010',10);
        """)

        conn.commit()
        print("✅ Database seeded successfully!")

    except Exception as e:
        conn.rollback()
        print("❌ Error during seeding:", e)

    finally:
        cursor.close()
        conn.close()
# Wait for Postgres server up
def wait_for_postgres(retries=10, delay=3):
    for attempt in range(retries):
        try:
            conn = get_server_connection()
            conn.close()
            print("✅ PostgreSQL server is ready!")
            return True
        except:
            print(f"⏳ Waiting for PostgreSQL server... {attempt+1}/{retries}")
            time.sleep(delay)
    return False

if __name__ == "__main__":
    if wait_for_postgres():
        create_database()
        create_tables()
        seed_database()
    else:
        print("❌ PostgreSQL server not ready. Exiting.")
