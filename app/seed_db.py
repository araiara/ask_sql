import psycopg2
from app.config import get_postgres_connection


def seed_database() -> None:
    conn = get_postgres_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS categories;
    """
    )
    conn.commit()

    # Create tables
    cursor.execute(
        """
    CREATE TABLE categories (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR(50) NOT NULL
    );
    
    CREATE TABLE products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        category_id INT NOT NULL REFERENCES categories(category_id),
        price NUMERIC(10,2) NOT NULL
    );
    
    CREATE TABLE customers (
        customer_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        customer_id INT NOT NULL REFERENCES customers(customer_id),
        order_date TIMESTAMP NOT NULL,
        status VARCHAR(20) NOT NULL
    );
    
    CREATE TABLE order_items (
        order_item_id SERIAL PRIMARY KEY,
        order_id INT NOT NULL REFERENCES orders(order_id),
        product_id INT NOT NULL REFERENCES products(product_id),
        quantity INT NOT NULL,
        unit_price NUMERIC(10,2) NOT NULL
    );
    """
    )
    conn.commit()

    # Insert sample data
    cursor.execute(
        """
    INSERT INTO categories (category_name) VALUES
    ('Electronics'), ('Clothing'), ('Books');

    INSERT INTO products (product_name, category_id, price) VALUES
    ('Laptop', 1, 1200.00),
    ('Smartphone', 1, 800.00),
    ('Jeans', 2, 50.00),
    ('T-Shirt', 2, 25.00),
    ('Novel', 3, 15.00);

    INSERT INTO customers (first_name, last_name, email) VALUES
    ('Alice', 'Johnson', 'alice@example.com'),
    ('Bob', 'Smith', 'bob@example.com'),
    ('Carol', 'Lee', 'carol@example.com');

    INSERT INTO orders (customer_id, order_date, status) VALUES
    (1, '2025-11-15 10:00:00', 'completed'),
    (2, '2025-11-20 14:30:00', 'completed'),
    (1, '2025-12-01 09:45:00', 'pending');

    INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 1200.00),
    (1, 5, 2, 15.00),
    (2, 3, 2, 50.00),
    (2, 4, 3, 25.00),
    (3, 2, 1, 800.00);
    """
    )
    conn.commit()

    print("Database seeded successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    seed_database()
