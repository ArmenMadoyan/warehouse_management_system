import os
import csv
import random
from faker import Faker

# Initialize Faker
faker = Faker()

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

# ------------- Table Generators -------------

def generate_product(n=100):
    with open("data/product.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "product_name", "description", "weight", "unit_cost", "unit_price"])
        for i in range(1, n+1):
            writer.writerow([
                i,
                faker.word().capitalize(),
                faker.text(max_nb_chars=100),
                round(random.uniform(0.1, 100.0), 2),
                round(random.uniform(5.0, 100.0), 2),
                round(random.uniform(10.0, 200.0), 2)
            ])

def generate_warehouse(n=10):
    with open("data/warehouse.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["warehouse_id", "warehouse_name", "warehouse_location"])
        for i in range(1, n+1):
            writer.writerow([
                i,
                faker.company(),
                faker.address().replace("\n", ", ")
            ])

def generate_inventory(product_count=100, warehouse_count=10):
    with open("data/inventory.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["warehouse_id", "product_id", "quantity_on_hand", "reorder_level"])
        for _ in range(product_count * 2):
            writer.writerow([
                random.randint(1, warehouse_count),
                random.randint(1, product_count),
                random.randint(0, 500),
                random.randint(0, 100)
            ])

def generate_app_user(n=20):
    with open("data/app_user.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "username", "password_hash", "full_name", "user_role"])
        for i in range(1, n+1):
            writer.writerow([
                i,
                faker.user_name(),
                faker.sha256(),
                faker.name(),
                random.choice(["Admin", "Manager", "Employee"])
            ])

def generate_client(n=50):
    with open("data/client.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["client_id", "client_name", "email", "phone"])
        for i in range(1, n+1):
            writer.writerow([
                i,
                faker.company(),
                faker.email(),
                faker.phone_number()
            ])

def generate_store(n=10):
    with open("data/store.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["store_id", "store_name", "store_location"])
        for i in range(1, n+1):
            writer.writerow([
                i,
                faker.company(),
                faker.address().replace("\n", ", ")
            ])

def generate_purchase_order(n=100, warehouse_count=10, user_count=20):
    with open("data/purchase_order.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["purchase_id", "purchase_date", "total_cost", "warehouse_id", "user_id"])
        for i in range(1, n+1):
            writer.writerow([
                i,
                faker.date_between(start_date='-1y', end_date='today'),
                round(random.uniform(500.0, 5000.0), 2),
                random.randint(1, warehouse_count),
                random.randint(1, user_count)
            ])

def generate_purchase_item(purchase_count=100, product_count=100):
    with open("data/purchase_item.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["purchase_id", "product_id", "unit_cost", "quantity"])
        for _ in range(purchase_count * 2):
            writer.writerow([
                random.randint(1, purchase_count),
                random.randint(1, product_count),
                round(random.uniform(5.0, 100.0), 2),
                random.randint(1, 100)
            ])

def generate_sale_order(n=100, client_count=50, store_count=10, user_count=20):
    with open("data/sale_order.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sale_id", "sale_date", "total_amount", "client_id", "store_id", "user_id"])
        for i in range(1, n+1):
            writer.writerow([
                i,
                faker.date_between(start_date='-1y', end_date='today'),
                round(random.uniform(500.0, 7000.0), 2),
                random.randint(1, client_count),
                random.randint(1, store_count),
                random.randint(1, user_count)
            ])

def generate_sale_item(sale_count=100, product_count=100):
    with open("data/sale_item.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sale_id", "product_id", "sale_price", "quantity"])
        for _ in range(sale_count * 2):
            writer.writerow([
                random.randint(1, sale_count),
                random.randint(1, product_count),
                round(random.uniform(10.0, 300.0), 2),
                random.randint(1, 50)
            ])

def generate_payment(sale_count=100):
    with open("data/payment.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["payment_id", "payment_date", "amount", "payment_method", "reference_number", "sale_id"])
        for i in range(1, sale_count+1):
            writer.writerow([
                i,
                faker.date_between(start_date='-1y', end_date='today'),
                round(random.uniform(500.0, 7000.0), 2),
                random.choice(["Credit Card", "Bank Transfer", "Cash", "PayPal"]),
                faker.uuid4(),
                i  # 1-1 mapping with sale_id
            ])

# ------------- Master Generator -------------

def generate_all():
    generate_product()
    generate_warehouse()
    generate_inventory()
    generate_app_user()
    generate_client()
    generate_store()
    generate_purchase_order()
    generate_purchase_item()
    generate_sale_order()
    generate_sale_item()
    generate_payment()

if __name__ == "__main__":
    generate_all()
    print("CSV files generated in /data folder!")