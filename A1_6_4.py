# -- coding: utf-8 --
import sqlite3
from datetime import datetime

DB_FILE = "store.db"

# Initialize database (create tables if they don't exist)
def init_db():
    """Create tables and insert dummy data if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Enable foreign key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create `customers` table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Create `products` table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            seller_id INTEGER NOT NULL,
            FOREIGN KEY (seller_id) REFERENCES customers(id) ON DELETE CASCADE
        )
    """)

    # Create `orders` table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            total_price REAL NOT NULL,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,  -- Ensures timestamp storage
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
        )
    """)

    # Create `order_items` table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)

    # Insert dummy customers
    customers_data = [
        ("John Doe",), ("Jane Smith",), ("Alice Johnson",), ("Bob Brown",),
        ("Charlie Wilson",), ("David Miller",), ("Emily Davis",), ("Frank Thomas",),
        ("Grace White",), ("Henry Clark",)
    ]
    cursor.executemany("INSERT OR IGNORE INTO customers (name) VALUES (?);", customers_data)

    # Insert dummy products
    products_data = [
        ("Laptop", "Dell Inspiron 15", 55000.00, 10, 1),
        ("Smartphone", "Samsung Galaxy S21", 65000.00, 15, 2),
        ("Headphones", "Sony WH-1000XM4", 15000.00, 20, 3),
        ("Tablet", "iPad Air", 45000.00, 8, 4),
        ("Smartwatch", "Apple Watch Series 7", 40000.00, 12, 5),
        ("Gaming Console", "PlayStation 5", 60000.00, 5, 6),
        ("Camera", "Canon EOS 1500D", 38000.00, 7, 7),
        ("Monitor", "LG UltraFine 4K", 35000.00, 9, 8),
        ("Keyboard", "Mechanical Gaming Keyboard", 5000.00, 25, 9),
        ("Mouse", "Logitech MX Master 3", 7000.00, 30, 10)
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO products (name, description, price, stock, seller_id) VALUES (?, ?, ?, ?, ?);",
        products_data
    )

    # Insert dummy orders
    orders_data = [
        (1, 55000.00, "2024-03-01 14:20:00"),
        (2, 65000.00, "2024-03-02 10:45:00"),
        (3, 15000.00, "2024-03-03 16:30:00"),
        (4, 45000.00, "2024-03-04 12:00:00"),
        (5, 40000.00, "2024-03-05 09:10:00"),
        (6, 60000.00, "2024-03-06 18:15:00"),
        (7, 38000.00, "2024-03-07 14:55:00"),
        (8, 35000.00, "2024-03-08 20:05:00"),
        (9, 5000.00, "2024-03-09 11:25:00"),
        (10, 7000.00, "2024-03-10 13:40:00")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO orders (customer_id, total_price, order_date) VALUES (?, ?, ?);",
        orders_data
    )

    # Insert dummy order items
    order_items_data = [
        (1, 1, 1, 55000.00),
        (2, 2, 1, 65000.00),
        (3, 3, 1, 15000.00),
        (4, 4, 1, 45000.00),
        (5, 5, 1, 40000.00),
        (6, 6, 1, 60000.00),
        (7, 7, 1, 38000.00),
        (8, 8, 1, 35000.00),
        (9, 9, 1, 5000.00),
        (10, 10, 1, 7000.00)
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?);",
        order_items_data
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()



# Database connection function
def connect_db():
    """Establish connection to SQLite database"""
    return sqlite3.connect(DB_FILE)

# Load products from SQLite
def load_products():
    """Fetch all products from the database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY id")
    products = cursor.fetchall()
    conn.close()
    return products

# Display product list
def display_products(products):
    """Display available products from SQLite"""
    print("\nAvailable Products:")
    print("-" * 40)
    for product in products:
        print("{}. {} - ₹{} (Stock: {} pieces)".format(product[0], product[1], product[3], product[4]))
    print("-" * 40)

# Add a new product (Seller Action)
def add_product():
    """Insert a new product into the database"""
    conn = connect_db()
    cursor = conn.cursor()

    name = input("Enter product name: ")
    price = float(input("Enter product price (in ₹): "))
    quantity = int(input("Enter product quantity (in pieces): "))
    description = input("Enter some description about your product: ")

    sql = "INSERT INTO products (name, description, price, stock, seller_id) VALUES (?, ?, ?, ?, ?)"
    values = (name, description, price, quantity, 3)  # Assuming seller ID = 3 (change as needed)

    cursor.execute(sql, values)
    conn.commit()

    print("{} added successfully!".format(name))

    cursor.close()
    conn.close()

# Purchase a product (Customer)
def purchase_product():
    """Allow customers to buy a product and update the database"""
    products = load_products()
    display_products(products)

    try:
        product_id = int(input("Enter the product ID to purchase: "))
        quantity = int(input("Enter quantity (in pieces): "))
        customer_name = input("Enter your name: ")

        conn = connect_db()
        cursor = conn.cursor()

        # Check if customer already exists
        cursor.execute("SELECT id FROM customers WHERE name = ?", (customer_name,))
        customer = cursor.fetchone()

        if customer:
            customer_id = customer[0]
        else:
            # Insert new customer and get their ID
            cursor.execute("INSERT INTO customers (name) VALUES (?)", (customer_name,))
            conn.commit()
            customer_id = cursor.lastrowid  # Get last inserted customer ID

        # Fetch the selected product
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()

        if product and product[4] >= quantity:  # product[4] is stock
            total_price = product[3] * quantity  # product[3] is price

            # Deduct purchased quantity from stock
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))

            # Insert order into orders table
            cursor.execute("INSERT INTO orders (customer_id, total_price) VALUES (?, ?)", (customer_id, total_price))
            order_id = cursor.lastrowid  # Get the last inserted order ID

            # Insert into order_items table
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", 
                           (order_id, product_id, quantity, product[3]))

            conn.commit()
            print("Purchase successful! You paid ₹{}.".format(total_price))
        else:
            print("Invalid product ID or insufficient stock.")

        cursor.close()
        conn.close()
    except ValueError:
        print("Invalid input. Please enter numbers for product ID and quantity.")

# Main menu
def main():
    init_db()  # Ensure database and tables are set up

    while True:
        print("\nInventory Management System")
        print("1. View Products")
        print("2. Add Product (Seller)")
        print("3. Purchase Product (Customer)")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            display_products(load_products())
        elif choice == "2":
            add_product()
        elif choice == "3":
            purchase_product()
        elif choice == "4":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()




