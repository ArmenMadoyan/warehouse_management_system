
# Warehouse Management System (WMS) - Fullstack Project

## Project Overview

This project implements a **Warehouse Management System (WMS)** using:
- **PostgreSQL** (for database backend)
- **Streamlit** (for frontend UI)
- **Docker Compose** (for service orchestration)
- **SQLAlchemy** (for database connection)

The system manages products, inventory, purchases, sales, clients, stores, and users. It provides real-time visibility into warehouse operations, revenue, top-selling products, stock levels, and client purchases.

---

## Project Structure

```
.
├── docker-compose.yml
├── Dockerfile
├── sql/
│   ├── ddl.sql
│   ├── dml.sql
│   └── dql.sql
├── front.py
└── README.md
```

- `sql/` folder contains database initialization scripts (DDL, DML, DQL).
- `front.py` provides the full web application frontend.
- `docker-compose.yml` orchestrates PostgreSQL, pgAdmin, and frontend services.

---

## Functionalities

- ✅ User Registration and Login
- ✅ View tables (products, warehouses, inventory, users, etc.)
- ✅ Low stock alerts
- ✅ Top-selling products
- ✅ Revenue reports (by product, by store, monthly)
- ✅ Client purchase history
- ✅ Logout functionality

---

## Setup Instructions

### 1. Prerequisites
- Docker and Docker Compose installed
- Internet access for pulling images

### 2. Start the Project
```bash
docker compose up -d --build
```

This command will:
- Start the PostgreSQL server
- Start pgAdmin UI
- Build and launch the Streamlit frontend

### 3. Initialize Database
The `sql/ddl.sql` and `sql/dml.sql` scripts will be automatically loaded into the PostgreSQL database via Docker.

## Accessing the Application

- **Frontend (Streamlit App)**: [http://localhost:8502](http://localhost:8502)
- **pgAdmin**: [http://localhost:5055](http://localhost:5055)

---

## Environment Variables

Database connection settings (already baked into `docker-compose.yml`):
- DB Name: `mydatabase`
- DB User: `myuser`
- DB Password: `mypassword`
- Host: `postgres`
- Port: `5432`

---

## Technologies Used

- Python 3.10
- PostgreSQL 15+
- SQLAlchemy
- Streamlit
- Docker + Docker Compose
- pgAdmin4

---

## Notes

- **Fully containerized**: No local installations required beyond Docker.
- **Modular frontend**: Easy to extend with additional functionalities like order placement, payment processing, inventory forecasting.

---

## Author

> Armen

