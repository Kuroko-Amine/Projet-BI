import pyodbc

DB_PATH = r"data/Northwind 2012.accdb"
CONN_STR = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={DB_PATH};"

try:
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    
    # List tables
    print("--- TABLES ---")
    for row in cursor.tables():
        if row.table_type == "TABLE":
            print(row.table_name)
            
    # Inspect Columns for key tables
    for table in ["Customers", "Orders", "Employees", "Order Details", "Products"]:
        print(f"\n--- COLUMNS: {table} ---")
        try:
            for row in cursor.columns(table=table):
                print(row.column_name)
        except Exception as e:
            print(f"Error reading {table}: {e}")
            
    conn.close()
except Exception as e:
    print("Connection failed:", e)
