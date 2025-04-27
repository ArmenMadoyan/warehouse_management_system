-- ====================================================
-- DML Script for WMS
-- ====================================================

TRUNCATE TABLE payment, sale_item, sale_order, purchase_item, purchase_order, inventory, store, client, app_user, warehouse, product RESTART IDENTITY CASCADE;

-- INSERT products
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

-- INSERT warehouses
INSERT INTO warehouse (warehouse_id, warehouse_name, warehouse_location) VALUES
  (1, 'Central Warehouse', 'Yerevan'),
  (2, 'North Warehouse', 'Gyumri'),
  (3, 'South Warehouse', 'Kapan');

-- INSERT inventory
INSERT INTO inventory (warehouse_id, product_id, quantity_on_hand, reorder_level) VALUES
  (1, 1, 181, 33),
  (1, 2, 179, 23),
  (1, 3, 113, 30),
  (1, 4, 6, 25),
  (1, 5, 51, 44),
  (1, 6, 75, 40),
  (1, 7, 54, 39),
  (1, 8, 104, 33),
  (1, 9, 2, 43),
  (1, 10, 117, 50),
  (2, 1, 72, 44),
  (2, 2, 121, 20),
  (2, 3, 93, 36),
  (2, 4, 195, 21),
  (2, 5, 180, 32),
  (2, 6, 10, 47),
  (2, 7, 139, 40),
  (2, 8, 27, 23),
  (2, 9, 130, 32),
  (2, 10, 191, 23),
  (3, 1, 13, 30),
  (3, 2, 43, 39),
  (3, 3, 88, 45),
  (3, 4, 180, 42),
  (3, 5, 106, 28),
  (3, 6, 34, 39),
  (3, 7, 0, 41),
  (3, 8, 171, 45),
  (3, 9, 44, 44),
  (3, 10, 131, 35);

-- INSERT users
INSERT INTO app_user (user_id, username, password_hash, full_name, user_role) VALUES
  (1, 'user1', 'md5hash', 'User 1', 'Accountant'),
  (2, 'user2', 'md5hash', 'User 2', 'Owner'),
  (3, 'user3', 'md5hash', 'User 3', 'Accountant'),
  (4, 'user4', 'md5hash', 'User 4', 'Accountant'),
  (5, 'user5', 'md5hash', 'User 5', 'Worker');

SELECT setval('app_user_user_id_seq', (SELECT MAX(user_id) FROM app_user));

-- INSERT clients
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

-- INSERT stores
INSERT INTO store (store_id, store_name, store_location) VALUES
  (1, 'Store A', 'Yerevan'),
  (2, 'Store B', 'Gyumri'),
  (3, 'Store C', 'Vanadzor');

-- INSERT purchase orders
INSERT INTO purchase_order (purchase_id, purchase_date, total_cost, warehouse_id, user_id) VALUES
  (1, '2024-11-22', 665.04, 1, 4),
  (2, '2024-05-06', 2416.38, 1, 1),
  (3, '2024-11-24', 1575.64, 3, 3),
  (4, '2025-01-03', 2623.74, 2, 3),
  (5, '2024-10-01', 1589.41, 2, 2),
  (6, '2024-03-15', 1118.66, 3, 5),
  (7, '2025-01-19', 2346.05, 1, 2),
  (8, '2024-09-20', 1300.11, 1, 1),
  (9, '2024-07-08', 2142.14, 3, 4),
  (10, '2025-04-03', 1123.37, 3, 2),
  (11, '2024-12-15', 2232.41, 2, 3),
  (12, '2025-01-07', 1830.88, 3, 1),
  (13, '2024-06-29', 2616.63, 1, 5),
  (14, '2024-08-12', 2354.39, 2, 4),
  (15, '2024-03-16', 2799.32, 1, 2),
  (16, '2024-03-16', 2799.32, 1, 2);

-- INSERT purchase items
INSERT INTO purchase_item (purchase_id, product_id, unit_cost, quantity) VALUES
  (1, 1, 13.44, 16),
  (1, 5, 6.92, 25),
  (1, 4, 19.27, 20),
  (2, 2, 44.42, 26),
  (2, 8, 39.29, 16),
  (2, 4, 19.27, 26),
  (3, 3, 8.91, 23),
  (3, 1, 13.44, 17),
  (3, 7, 46.79, 19),
  (4, 4, 19.27, 22),
  (4, 2, 44.42, 13),
  (4, 8, 39.29, 10),
  (5, 5, 6.92, 28),
  (5, 6, 42.37, 14),
  (5, 3, 8.98, 15),
  (6, 6, 42.37, 17),
  (6, 9, 12.34, 8),
  (6, 1, 13.44, 12),
  (7, 7, 46.79, 21),
  (7, 3, 8.98, 16),
  (7, 10, 18.07, 14),
  (8, 8, 39.29, 19),
  (8, 2, 44.42, 18),
  (8, 6, 42.37, 20),
  (9, 9, 12.34, 24),
  (9, 5, 6.92, 11),
  (9, 4, 19.27, 13),
  (10, 10, 18.07, 15),
  (10, 1, 13.44, 12),
  (10, 7, 46.79, 17),
  (11, 5, 6.92, 16),
  (11, 8, 39.29, 18),
  (11, 3, 8.98, 14),
  (12, 2, 44.42, 20),
  (12, 4, 19.27, 22),
  (12, 9, 12.34, 19),
  (13, 3, 8.98, 18),
  (13, 7, 46.79, 21),
  (13, 1, 13.44, 15),
  (14, 4, 19.27, 17),
  (14, 2, 44.42, 13),
  (14, 8, 39.29, 12),
  (15, 1, 13.44, 16),
  (15, 6, 42.37, 19),
  (15, 3, 8.98, 18),
  (16, 4, 19.27, 30);

-- INSERT sale orders
INSERT INTO sale_order (sale_id, sale_date, total_amount, client_id, store_id, user_id) VALUES
  (1, '2025-01-10', 360.31, 1, 1, 2),
  (2, '2025-02-14', 477.58, 2, 2, 3),
  (3, '2025-03-03', 248.39, 3, 3, 4),
  (4, '2025-01-20', 216.85, 4, 1, 1),
  (5, '2025-02-25', 387.12, 5, 2, 5),
  (6, '2025-03-15', 341.96, 6, 3, 2),
  (7, '2025-04-05', 239.28, 7, 1, 3),
  (8, '2025-04-10', 243.95, 8, 2, 4),
  (9, '2025-04-12', 330.30, 9, 3, 1),
  (10, '2025-04-15', 412.50, 10, 1, 5);

-- INSERT sale items
INSERT INTO sale_item (sale_id, product_id, sale_price, quantity) VALUES
  (1, 1, 137.97, 2),
  (1, 5, 84.37, 1),
  (2, 2, 106.02, 3),
  (2, 4, 79.76, 2),
  (3, 1, 137.97, 1),
  (3, 3, 97.97, 2),
  (4, 4, 79.76, 1),
  (4, 2, 106.02, 2),
  (5, 5, 84.37, 3),
  (5, 6, 75.21, 2),
  (6, 6, 75.21, 1),
  (6, 9, 120.58, 2),
  (7, 7, 113.45, 1),
  (7, 10, 145.96, 2),
  (8, 8, 103.40, 3),
  (8, 2, 106.02, 1),
  (9, 9, 120.58, 2),
  (9, 5, 84.37, 1),
  (10, 10, 145.96, 2);

-- INSERT payments
INSERT INTO payment (payment_id, payment_date, amount, payment_method, reference_number, sale_id) VALUES
  (1,  '2025-01-11', 360.31, 'Cash',         'REF0001', 1),
  (2,  '2025-02-15', 477.58, 'Credit Card',  'REF0002', 2),
  (3,  '2025-03-04', 248.39, 'Bank Transfer','REF0003', 3),
  (4,  '2025-01-21', 216.85, 'Cash',         'REF0004', 4),
  (5,  '2025-02-26', 387.12, 'Credit Card',  'REF0005', 5),
  (6,  '2025-03-16', 341.96, 'Bank Transfer','REF0006', 6),
  (7,  '2025-04-06', 239.28, 'Cash',         'REF0007', 7),
  (8,  '2025-04-11', 243.95, 'Credit Card',  'REF0008', 8),
  (9,  '2025-04-13', 330.30, 'Bank Transfer','REF0009', 9),
  (10, '2025-04-16', 412.50, 'Cash',         'REF0010', 10);
