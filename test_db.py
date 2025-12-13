import pyodbc
server = r"asus_zakami\SQLAMINE"
try:
    conn = pyodbc.connect(f"DRIVER={{SQL Server}};SERVER={server};DATABASE=master;Trusted_Connection=yes;")
    print("Connected to master successfully")
    conn.close()
except Exception as e:
    print("Failed to connect to master:", e)
