import sqlite3
import os 
def run_a10(database_path: str, type: str, output_path: str):
    """
    Calculate the total sales for a particular ticket type in an SQLite database and write the result to a file.
    """ 
    def is_allowed_path(file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith("/data/")
            
    if not is_allowed_path(database_path) or not is_allowed_path(output_path):
        raise PermissionError(f"Access outside /data/ is not allowed: {database_path} or {output_path}")
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        # Query to calculate total sales for the specified ticket type
        query = """
        SELECT SUM(units * price) FROM tickets WHERE type = ?
        """
        cursor.execute(query, (type,))
        result = cursor.fetchone()
        total_sales = result[0] if result[0] is not None else 0
        
        # Write the result to the output file
        with open(output_path, "w") as file:
            file.write(str(total_sales))
        
        print(f"Total sales for '{type}' tickets: {total_sales}")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()
