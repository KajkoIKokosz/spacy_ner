import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'geocoder',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

def execute_query(query):
    """
    Executes the provided SQL query and returns a list of results.

    Parameters:
    query (str): The SQL raw query to be executed.

    Returns:
    list: A list of results.
    """
    results = []

    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(**db_params)

        # Create a cursor object
        cur = conn.cursor()

        # Execute the SQL query
        cur.execute(query)

        # Fetch all rows from the result set
        results = cur.fetchall()

    except psycopg2.Error as e:
        print("Error: Unable to execute the query.")
        print(e)

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

    return results

# Example usage
