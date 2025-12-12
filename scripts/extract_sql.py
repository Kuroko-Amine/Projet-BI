import pandas as pd
import os
import pyodbc
from database_manager import get_sql_conn_str, SQL_DATABASE
from settings import DATA_DIR

def extract_from_sql():
    """Extracts tables from SQL Server and saves them as CSVs."""
    print("--- Starting Extraction from SQL Server ---")
    
    output_dir = os.path.join(DATA_DIR, "extracted")
    os.makedirs(output_dir, exist_ok=True)
    
    conn_str = get_sql_conn_str(SQL_DATABASE)
    
    try:
        conn = pyodbc.connect(conn_str)
        
        tables = ["DimCustomer", "DimEmployee", "DimDate", "FactOrders"]
        
        for table in tables:
            print(f"Extracting {table}...")
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, conn)
            
            output_path = os.path.join(output_dir, f"{table}.csv")
            df.to_csv(output_path, index=False)
            print(f"Saved {table} to {output_path}")
            
        conn.close()
        print("--- Extraction Complete ---")
        
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
        raise

if __name__ == "__main__":
    extract_from_sql()
