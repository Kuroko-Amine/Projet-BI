import sys
print(f"Executable: {sys.executable}")
try:
    import pyodbc
    print(f"pyodbc imported successfully: {pyodbc}")
except ImportError as e:
    print(f"Error importing pyodbc: {e}")
    print("sys.path follows:")
    for p in sys.path:
        print(p)
