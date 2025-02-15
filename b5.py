import sqlite3 
import duckdb

def run_sql_query(db_type: str, db_path: str, query: str):
    try:
        if db_type == "sqlite":
            conn = sqlite3.connect(db_path)
        elif db_type == "duckdb":
            conn = duckdb.connect(db_path)
        else:
            raise #HTTPException(status_code=400, detail="Unsupported database type")
        
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        return {"results": results}
    except:
        pass 