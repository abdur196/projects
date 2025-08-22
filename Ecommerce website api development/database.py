import pyodbc

# Function to get the database connection
def get_db_connection():
    print("Trying to connect to the database...")  # Debug line
    try:
        connection = pyodbc.connect(
            driver='{ODBC Driver 17 for SQL Server}',  # Driver for SQL Server
            server='localhost',  # or your SQL Server hostname
            database='ecommerce',  # Database name
            trusted_connection='yes'  # Use Windows Authentication
        )

        if connection:
            print("✅ Connection successful!")
            return connection
        else:
            print("❌ Connection failed!")
            return None
    except pyodbc.Error as err:
        print(f"❗ Error connecting: {err}")
        return None

# Function to fetch all products
def get_all_products():
    connection = get_db_connection()
    if connection:
        print("Fetching products...")  # Debugging line
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")  # Query to get all products
        products = cursor.fetchall()  # Fetch all rows
        cursor.close()
        connection.close()
        return products  # Return the list of products
    else:
        print("Connection not established. Cannot fetch products.")
    return None  # If the connection failed

# Function to add a new product
def add_product(name, price, category, stock):
    print("Adding product...")  # Debugging line
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO products (name, price, category, stock)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (name, price, category, stock))  # Use ? for SQL Server params
        connection.commit()
        cursor.close()
        connection.close()
        print("Product added successfully!")
        return True
    else:
        print("Failed to add product. Connection failed.")
    return False

# Function to update inventory
def update_inventory(product_id, quantity_change):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        INSERT INTO inventory (product_id, quantity_change)
        VALUES (?, ?)
        """
        cursor.execute(query, (product_id, quantity_change))  # Use ? for SQL Server params
        connection.commit()
        cursor.close()
        connection.close()
        print("Inventory updated successfully!")
        return True
    print("Failed to update inventory. Connection failed.")
    return False

# Function to get sales for a specific product
def get_sales_by_product(product_id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        SELECT p.name, SUM(s.total_amount) AS total_sales
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE s.product_id = ?
        GROUP BY p.name
        """
        cursor.execute(query, (product_id,))
        sales = cursor.fetchone()  # Fetch the first result (since it's grouped by product)
        cursor.close()
        connection.close()
        return sales
    print("Failed to get sales data. Connection failed.")
    return None  # If the connection failed or no sales were found

if __name__ == "__main__":
    # Example test: add a product
    print("Testing database functions...")  # Debugging line

    product_added = add_product("Test Product", 29.99, "Electronics", 100)
    print("Product added:", product_added)

    products = get_all_products()
    print("All products:", products)

    inventory_updated = update_inventory(1, -10)  # Assuming product with ID 1 exists
    print("Inventory updated:", inventory_updated)

    sales = get_sales_by_product(1)
    print("Sales for product 1:", sales)
