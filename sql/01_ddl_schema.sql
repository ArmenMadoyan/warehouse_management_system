-- ================================================
-- DDL Script for Warehouse Management System
-- ================================================

DROP TABLE IF EXISTS payment CASCADE;
DROP TABLE IF EXISTS sale_item CASCADE;
DROP TABLE IF EXISTS sale_order CASCADE;
DROP TABLE IF EXISTS purchase_item CASCADE;
DROP TABLE IF EXISTS purchase_order CASCADE;
DROP TABLE IF EXISTS store CASCADE;
DROP TABLE IF EXISTS client CASCADE;
DROP TABLE IF EXISTS app_user CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS warehouse CASCADE;
DROP TABLE IF EXISTS product CASCADE;

-- ================================
-- DDL Script for Warehouse Management System
-- ================================

-- 1. PRODUCT
CREATE TABLE product (
  product_id   SERIAL        PRIMARY KEY,
  product_name VARCHAR(100)  NOT NULL,
  description  TEXT,
  weight       DECIMAL(8,2) NOT NULL CHECK (weight >= 0),
  unit_cost    DECIMAL(10,2) NOT NULL CHECK (unit_cost >= 0),
  unit_price   DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0)
);

-- 2. WAREHOUSE
CREATE TABLE warehouse (
  warehouse_id   SERIAL       PRIMARY KEY,
  warehouse_name VARCHAR(100) NOT NULL,
  warehouse_location VARCHAR(200)
);

-- 3. INVENTORY (junction: warehouse ↔ product)
CREATE TABLE inventory (
  warehouse_id     INT NOT NULL,
  product_id       INT NOT NULL,
  quantity_on_hand INT DEFAULT 0 CHECK (quantity_on_hand >= 0),
  reorder_level    INT DEFAULT 0 CHECK (reorder_level >= 0),
  PRIMARY KEY (warehouse_id, product_id),
  FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id),
  FOREIGN KEY (product_id)   REFERENCES product(product_id)
);

-- 4. APP_USER
CREATE TABLE app_user (
  user_id       SERIAL       PRIMARY KEY,
  username      VARCHAR(50)  NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  full_name     VARCHAR(100) NOT NULL,
  user_role     VARCHAR(50)  NOT NULL
);

-- 5. CLIENT
CREATE TABLE client (
  client_id   SERIAL       PRIMARY KEY,
  client_name VARCHAR(100) NOT NULL,
  email       VARCHAR(100),
  phone       VARCHAR(20)
);

-- 6. STORE
CREATE TABLE store (
  store_id      SERIAL       PRIMARY KEY,
  store_name    VARCHAR(100) NOT NULL,
  store_location VARCHAR(200)
);

-- 7. PURCHASE_ORDER
CREATE TABLE purchase_order (
  purchase_id   SERIAL       PRIMARY KEY,
  purchase_date DATE         NOT NULL,
  total_cost    DECIMAL(12,2) NOT NULL CHECK (total_cost >= 0),
  warehouse_id  INT          NOT NULL,
  user_id       INT          NOT NULL,
  FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id),
  FOREIGN KEY (user_id)      REFERENCES app_user(user_id)
);

-- 8. PURCHASE_ITEM (junction: purchase_order ↔ product)
CREATE TABLE purchase_item (
  purchase_id INT          NOT NULL,
  product_id  INT          NOT NULL,
  unit_cost   DECIMAL(10,2) NOT NULL CHECK (unit_cost >= 0),
  quantity    INT          NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (purchase_id, product_id),
  FOREIGN KEY (purchase_id) REFERENCES purchase_order(purchase_id),
  FOREIGN KEY (product_id)  REFERENCES product(product_id)
);

-- 9. SALE_ORDER
CREATE TABLE sale_order (
  sale_id      SERIAL       PRIMARY KEY,
  sale_date    DATE         NOT NULL,
  total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),
  client_id    INT          NOT NULL,
  store_id     INT          NOT NULL,
  user_id      INT          NOT NULL,
  FOREIGN KEY (client_id) REFERENCES client(client_id),
  FOREIGN KEY (store_id)  REFERENCES store(store_id),
  FOREIGN KEY (user_id)   REFERENCES app_user(user_id)
);

-- 10. SALE_ITEM (junction: sale_order ↔ product)
CREATE TABLE sale_item (
  sale_id    INT          NOT NULL,
  product_id INT          NOT NULL,
  sale_price DECIMAL(10,2) NOT NULL CHECK (sale_price >= 0),
  quantity   INT          NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (sale_id, product_id),
  FOREIGN KEY (sale_id)    REFERENCES sale_order(sale_id),
  FOREIGN KEY (product_id) REFERENCES product(product_id)
);

-- 11. PAYMENT
CREATE TABLE payment (
  payment_id       SERIAL       PRIMARY KEY,
  payment_date     DATE         NOT NULL,
  amount           DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
  payment_method   VARCHAR(50),
  reference_number VARCHAR(100),
  sale_id          INT          NOT NULL UNIQUE,
  FOREIGN KEY (sale_id) REFERENCES sale_order(sale_id)
);
