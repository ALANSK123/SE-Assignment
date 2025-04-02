# 🏪 Inventory Management System  

A simple **Inventory Management System** built using **Python** and **SQLite3**.  
This system allows sellers to add products, customers to make purchases, and stores order details in a structured database.  

## 🎯 Project Overview  

This project is designed to provide a basic inventory management system that includes:  

- **Product Catalog**: View available products with details like price and stock.  
- **Seller Management**: Allows sellers to add new products to the inventory.  
- **Customer Order Processing**: Customers can purchase products, and stock updates automatically.  
- **Order Tracking**: Orders and order items are stored and managed in an SQLite database.  
- **Database Persistence**: Data is stored in `store.db`, ensuring no data loss between runs.  

---

## 🛠️ Technologies Used  

- **Python 3**  
- **SQLite3 (Database)**  

---

## 🚀 Features  

✅ **Database-Driven**: Uses SQLite3 for data storage and retrieval.  
✅ **CRUD Operations**: Sellers can add products; customers can purchase them.  
✅ **User Interaction**: Command-line interface for easy navigation.  
✅ **Automatic Stock Management**: Updates stock levels after purchases.  
✅ **Error Handling**: Ensures smooth user input and database transactions.  

---

## 📂 Project Structure  

📦 inventory-management
│-- 📄 inventory.py # Main application script
│-- 📄 store.db # SQLite database (created automatically)
│-- 📄 README.md # Project documentation


---

# 📸 Screenshots  

### 🏠 Main Menu  
![Main Menu](Screen_shots/Main_Menu%20.png)  

### 📦 Viewing Products  
![View Products](Screen_shots/Viewing_Products%20.png)  

### 🛒 Purchasing a Product  
![Purchase Product](Screen_shots/Purchasing_a_Product%20.png)  

---

## 🏗️ Database Schema  

The system consists of **four main tables** in SQLite:  

### 🧑‍💼 `customers` (Stores customer details)  
| Column | Type | Description |  
|---------|------|-------------|  
| `id` | INTEGER (Primary Key) | Unique customer ID |  
| `name` | TEXT (Unique) | Customer name |  

### 📦 `products` (Stores product information)  
| Column | Type | Description |  
|---------|------|-------------|  
| `id` | INTEGER (Primary Key) | Unique product ID |  
| `name` | TEXT | Product name |  
| `description` | TEXT | Product details |  
| `price` | REAL | Product price (₹) |  
| `stock` | INTEGER | Available quantity |  
| `seller_id` | INTEGER (Foreign Key) | Seller reference (from `customers`) |  

### 🛒 `orders` (Tracks customer purchases)  
| Column | Type | Description |  
|---------|------|-------------|  
| `id` | INTEGER (Primary Key) | Unique order ID |  
| `customer_id` | INTEGER (Foreign Key) | Buyer reference |  
| `total_price` | REAL | Total cost of order |  
| `order_date` | TEXT | Timestamp of order (Auto-generated) |  

### 📜 `order_items` (Stores ordered products)  
| Column | Type | Description |  
|---------|------|-------------|  
| `id` | INTEGER (Primary Key) | Unique order item ID |  
| `order_id` | INTEGER (Foreign Key) | Order reference |  
| `product_id` | INTEGER (Foreign Key) | Purchased product reference |  
| `quantity` | INTEGER | Quantity bought |  
| `price` | REAL | Price per unit |  

### In sqlite3
- .system cls (for screen clear)
- .tables (to see all tables)
- .mode box (to change the format)

- (query for seeing all purchased by name)

SELECT 
    o.id AS order_id, 
    c.name AS customer_name, 
    p.name AS product_name, 
    oi.quantity, 
    oi.price AS price_per_unit, 
    (oi.quantity * oi.price) AS total_price, 
    o.order_date
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
JOIN customers c ON o.customer_id = c.id
ORDER BY o.order_date DESC;


---

## 📜 License  

This project is licensed under the **MIT License**.  
Copyright (c) 2025 **Team 10, Group A1**  
- **Nikhil Sah**   
- **Himadri Mondal**
- **Alangir Sk**  

See the full **[LICENSE](LICENSE)** file for more details. 

---

## 🔧 Installation & Setup  

### 1️⃣ Clone the Repository  
```sh
git clone [text](https://github.com/Nikhil-JUIT27/SE_LAB_2025_A1_06_Repo)
cd Q1

## Author
Alangir Sk with Chat Gpt.
