import os
import sqlite3
import duckdb
import pandas as pd

def run_b5(query: str, db_type: str, db_path: str = None, output_path: str = None):
    try:
        # Set default db_path if not provided
        if db_path is None:
            db_path = "default.db"  # Modify as per your preferred default database path
        
        # Ensure the database type is supported
        if db_type not in ["sqlite", "duckdb"]:
            raise ValueError(f"Unsupported database type: {db_type}. Only 'sqlite' and 'duckdb' are allowed.")
        
        # Read the query if it's a file path
        if os.path.exists(query):
            with open(query, "r", encoding="utf-8") as file:
                query = file.read().strip()
        
        # Choose the correct database connection
        if db_type == "sqlite":
            conn = sqlite3.connect(db_path)
        else:  # db_type == "duckdb"
            conn = duckdb.connect(db_path)
        
        # Execute the query and fetch results
        df = pd.read_sql_query(query, conn)
        
        # Set default output path if not provided
        if output_path is None:
            output_path = "output.csv"
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save results to CSV
        df.to_csv(output_path, index=False)
        print(f"Query results saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

# Example Usage:
# run_sql_query("SELECT * FROM users", "sqlite", "database.sqlite", "output.csv")
# run_sql_query("query.sql", "duckdb", "database.duckdb", "output.csv")
