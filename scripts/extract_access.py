import pandas as pd
import pyodbc
import os
from settings import DATA_DIR

DB_PATH = os.path.join(DATA_DIR, "Northwind 2012.accdb")
CONN_STR = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH};"

def get_access_conn():
    try:
        return pyodbc.connect(CONN_STR)
    except Exception as e:
        print(f"[ERROR] Connection to Access failed: {e}")
        raise

def extract_from_access():
    """Extracts tables from Access DB and saves them as CSVs."""
    print("--- Starting Extraction from Access Database ---")
    
    output_dir = os.path.join(DATA_DIR, "extracted")
    os.makedirs(output_dir, exist_ok=True)
    
    conn = get_access_conn()
    
    # List of tables to extract based on inspection
    tables = ["Customers", "Employees", "Orders", "Order Details", "Products"]
    
    try:
        for table in tables:
            print(f"Extracting {table}...")
            # Enclose table name in brackets to handle spaces like 'Order Details'
            query = f"SELECT * FROM [{table}]"
            df = pd.read_sql(query, conn)
            
            # Sanitize filename (remove spaces)
            safe_name = table.replace(" ", "_")
            output_path = os.path.join(output_dir, f"Access_{safe_name}.csv")
            
            df.to_csv(output_path, index=False)
            print(f"Saved {table} to {output_path}")
            
    except Exception as e:
        print(f"[ERROR] Extraction failed during processing: {e}")
    finally:
        conn.close()
        print("--- Access Extraction Complete ---")

if __name__ == "__main__":
    extract_from_access()
