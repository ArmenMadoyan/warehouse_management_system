-- ================================================
-- DQL Script for WMS
-- ================================================

-- 1. User Registration & Authentication
-- =================================
CREATE OR REPLACE FUNCTION register_user(
  _username    VARCHAR,
  _password    VARCHAR,
  _full_name   VARCHAR,
  _user_role   VARCHAR
) RETURNS app_user AS $$
DECLARE
  new_u app_user;
BEGIN
  INSERT INTO app_user (username, password_hash, full_name, user_role)
    VALUES (_username, _password, _full_name, _user_role)
    RETURNING * INTO new_u;
  RETURN new_u;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION authenticate_user(
  _username    VARCHAR,
  _password    VARCHAR
) RETURNS BOOLEAN AS $$
DECLARE
  cnt INT;
BEGIN
  SELECT COUNT(*) INTO cnt
    FROM app_user
   WHERE username = _username
     AND password_hash = _password;
  RETURN (cnt = 1);
END;
$$ LANGUAGE plpgsql;

-- 2. Product Management
-- ====================
CREATE OR REPLACE FUNCTION add_product(
  _name     VARCHAR,
  _desc     TEXT,
  _weight   DECIMAL,
  _cost     DECIMAL,
  _price    DECIMAL
) RETURNS product AS $$
DECLARE
  p product;
BEGIN
  INSERT INTO product (product_name, description, weight, unit_cost, unit_price)
    VALUES (_name, _desc, _weight, _cost, _price)
    RETURNING * INTO p;
  RETURN p;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_product(
  _id       INT,
  _name     VARCHAR,
  _desc     TEXT,
  _weight   DECIMAL,
  _cost     DECIMAL,
  _price    DECIMAL
) RETURNS VOID AS $$
BEGIN
  UPDATE product
     SET product_name = _name,
         description  = _desc,
         weight       = _weight,
         unit_cost    = _cost,
         unit_price   = _price
   WHERE product_id = _id;
END;
$$ LANGUAGE plpgsql;

-- 3. Inventory Management & Stock Alerts
-- ======================================
-- Current inventory status by warehouse
-- Example: SELECT * FROM inventory_status();
CREATE OR REPLACE VIEW inventory_status AS
SELECT i.warehouse_id,
       w.warehouse_name,
       i.product_id,
       p.product_name,
       i.quantity_on_hand,
       i.reorder_level
  FROM inventory i
  JOIN warehouse w ON i.warehouse_id = w.warehouse_id
  JOIN product   p ON i.product_id   = p.product_id;

-- Low-stock alerts
CREATE OR REPLACE FUNCTION get_reorder_alerts()
RETURNS TABLE(
  warehouse_id      INT,
  warehouse_name    VARCHAR,
  product_id        INT,
  product_name      VARCHAR,
  quantity_on_hand  INT,
  reorder_level     INT
) AS $$
BEGIN
  RETURN QUERY
    SELECT i.warehouse_id,
           w.warehouse_name,
           i.product_id,
           p.product_name,
           i.quantity_on_hand,
           i.reorder_level
      FROM inventory i
      JOIN warehouse w ON i.warehouse_id = w.warehouse_id
      JOIN product   p ON i.product_id   = p.product_id
     WHERE i.quantity_on_hand < i.reorder_level;
END;
$$ LANGUAGE plpgsql;

-- 4. Purchase Order Processing
-- ============================
CREATE OR REPLACE FUNCTION record_purchase(
  _p_date    DATE,
  _warehouse INT,
  _user      INT,
  _items     JSON -- [{"product_id":1,"unit_cost":10.5,"quantity":5},...]
) RETURNS VOID AS $$
DECLARE
  new_po   INT;
  item     JSON;
BEGIN
  INSERT INTO purchase_order (purchase_date, total_cost, warehouse_id, user_id)
    VALUES (_p_date, 0, _warehouse, _user)
    RETURNING purchase_id INTO new_po;

  FOR item IN SELECT * FROM json_array_elements(_items)
  LOOP
    INSERT INTO purchase_item (purchase_id, product_id, unit_cost, quantity)
      VALUES (
        new_po,
        (item->>'product_id')::INT,
        (item->>'unit_cost')  ::DECIMAL,
        (item->>'quantity')   ::INT
      );

    UPDATE inventory
       SET quantity_on_hand = quantity_on_hand + (item->>'quantity')::INT
     WHERE warehouse_id = _warehouse
       AND product_id   = (item->>'product_id')::INT;
  END LOOP;

  UPDATE purchase_order
     SET total_cost = (
       SELECT SUM(unit_cost * quantity)
         FROM purchase_item
        WHERE purchase_id = new_po
     )
   WHERE purchase_id = new_po;
END;
$$ LANGUAGE plpgsql;

-- 5. Sales Order Management
-- =========================
CREATE OR REPLACE FUNCTION record_sale(
  _s_date    DATE,
  _client    INT,
  _store     INT,
  _user      INT,
  _items     JSON -- [{"product_id":1,"sale_price":20.5,"quantity":2},...]
) RETURNS VOID AS $$
DECLARE
  new_so   INT;
  item     JSON;
BEGIN
  INSERT INTO sale_order (sale_date, total_amount, client_id, store_id, user_id)
    VALUES (_s_date, 0, _client, _store, _user)
    RETURNING sale_id INTO new_so;

  FOR item IN SELECT * FROM json_array_elements(_items)
  LOOP
    INSERT INTO sale_item (sale_id, product_id, sale_price, quantity)
      VALUES (
        new_so,
        (item->>'product_id')::INT,
        (item->>'sale_price')  ::DECIMAL,
        (item->>'quantity')    ::INT
      );

    -- Deduct from inventory (assumes central warehouse usage)
    UPDATE inventory
       SET quantity_on_hand = quantity_on_hand - (item->>'quantity')::INT
     WHERE warehouse_id = 1 /* adjust as needed */
       AND product_id   = (item->>'product_id')::INT;
  END LOOP;

  UPDATE sale_order
     SET total_amount = (
       SELECT SUM(sale_price * quantity)
         FROM sale_item
        WHERE sale_id = new_so
     )
   WHERE sale_id = new_so;
END;
$$ LANGUAGE plpgsql;

-- Stock availability check
CREATE OR REPLACE FUNCTION is_in_stock(
  _product  INT,
  _warehouse INT,
  _qty       INT
) RETURNS BOOLEAN AS $$
DECLARE
  avail INT;
BEGIN
  SELECT quantity_on_hand INTO avail
    FROM inventory
   WHERE product_id   = _product
     AND warehouse_id = _warehouse;
  RETURN (avail >= _qty);
END;
$$ LANGUAGE plpgsql;

-- 6. Payment & Order Tracking
-- ==========================
-- Payment status summary
CREATE OR REPLACE VIEW payment_status AS
SELECT so.sale_id,
       so.sale_date,
       so.total_amount,
       CASE WHEN p.payment_id IS NULL THEN 'Pending' ELSE 'Completed' END AS status,
       p.payment_date,
       p.amount
  FROM sale_order so
  LEFT JOIN payment p ON so.sale_id = p.sale_id;

-- 7. Reporting & Insights
-- =======================
-- Top-selling products (by units)
-- Example: SELECT * FROM top_selling_products(10);
CREATE OR REPLACE FUNCTION top_selling_products(_limit INT)
RETURNS TABLE(product_id INT, product_name VARCHAR, total_units_sold BIGINT) AS $$
BEGIN
  RETURN QUERY
    SELECT si.product_id,
           p.product_name,
           SUM(si.quantity) AS total_units_sold
      FROM sale_item si
      JOIN product p ON si.product_id = p.product_id
     GROUP BY si.product_id, p.product_name
     ORDER BY total_units_sold DESC
     LIMIT _limit;
END;
$$ LANGUAGE plpgsql;

-- Revenue by product
CREATE OR REPLACE VIEW revenue_by_product AS
SELECT si.product_id,
       p.product_name,
       SUM(si.quantity * si.sale_price) AS revenue
  FROM sale_item si
  JOIN product p ON si.product_id = p.product_id
 GROUP BY si.product_id, p.product_name;

-- Revenue by store
CREATE OR REPLACE VIEW revenue_by_store AS
SELECT so.store_id,
       st.store_name,
       SUM(si.quantity * si.sale_price) AS revenue
  FROM sale_item si
  JOIN sale_order so ON si.sale_id = so.sale_id
  JOIN store st ON so.store_id = st.store_id
 GROUP BY so.store_id, st.store_name;

-- Monthly revenue trend
CREATE OR REPLACE VIEW monthly_revenue AS
SELECT date_trunc('month', sale_date) AS month,
       SUM(total_amount)                       AS revenue
  FROM sale_order
 GROUP BY month
 ORDER BY month;

-- Inventory health report (below reorder)
CREATE OR REPLACE VIEW inventory_health AS
SELECT i.warehouse_id,
       w.warehouse_name,
       i.product_id,
       p.product_name,
       i.quantity_on_hand,
       i.reorder_level
  FROM inventory i
  JOIN warehouse w ON i.warehouse_id = w.warehouse_id
  JOIN product   p ON i.product_id   = p.product_id
 WHERE i.quantity_on_hand < i.reorder_level;

-- Client purchase history
CREATE OR REPLACE FUNCTION client_history(_client INT)
RETURNS TABLE(
  sale_id     INT,
  sale_date   DATE,
  product_id  INT,
  product_name VARCHAR,
  quantity    INT,
  sale_price  DECIMAL
) AS $$
BEGIN
  RETURN QUERY
    SELECT so.sale_id,
           so.sale_date,
           si.product_id,
           p.product_name,
           si.quantity,
           si.sale_price
      FROM sale_order so
      JOIN sale_item si ON so.sale_id = si.sale_id
      JOIN product   p  ON si.product_id = p.product_id
     WHERE so.client_id = _client
     ORDER BY so.sale_date;
END;
$$ LANGUAGE plpgsql;

-- ================================================
-- End of DQL Script
-- ================================================
