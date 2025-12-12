import pyodbc
print("Installed ODBC Drivers:")
for d in pyodbc.drivers():
    print(d)
