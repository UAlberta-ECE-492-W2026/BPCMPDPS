import pandas as pd
import psycopg2

conn = None
try:
    # Connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    connection = psycopg2.connect(
        host="your_host",
        database="your_database_name",
        user="your_username",
        password="your_password",
        port="5432"
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a query (example)
    cursor.execute('SELECT version()')

    # Fetch and print the result
    db_version = cursor.fetchone()
    print(f"Connected to: {db_version}")

    # Close the cursor
    cursor.close()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the connection is closed
    if conn is not None:
        connection.close()
        print('Database connection closed.')

