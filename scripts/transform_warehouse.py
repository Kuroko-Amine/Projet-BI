import pandas as pd
import os
from settings import DATA_DIR

def transform_and_load_warehouse():
    """Reads extracted CSVs, merges them, and saves to warehouse."""
    print("--- Starting Transformation and Loading to Warehouse ---")
    
    extracted_dir = os.path.join(DATA_DIR, "extracted")
    warehouse_dir = os.path.join(DATA_DIR, "warehouse")
    os.makedirs(warehouse_dir, exist_ok=True)
    
    try:
        # Load extracted data
        print("Loading extracted CSVs...")
        dim_customer = pd.read_csv(os.path.join(extracted_dir, "DimCustomer.csv"))
        dim_employee = pd.read_csv(os.path.join(extracted_dir, "DimEmployee.csv"))
        dim_date = pd.read_csv(os.path.join(extracted_dir, "DimDate.csv"))
        fact_orders = pd.read_csv(os.path.join(extracted_dir, "FactOrders.csv"))
        
        # Merge Data
        # FactOrders -> DimCustomer
        print("Merging FactOrders with DimCustomer...")
        merged = fact_orders.merge(dim_customer, on="CustomerId", how="left")
        
        # Merge -> DimEmployee
        print("Merging with DimEmployee...")
        merged = merged.merge(dim_employee, on="EmployeeId", how="left")
        
        # Merge -> DimDate
        print("Merging with DimDate...")
        merged = merged.merge(dim_date, on="DateId", how="left")
        
        # Save to Warehouse
        output_path = os.path.join(warehouse_dir, "merged_northwind.csv")
        merged.to_csv(output_path, index=False)
        print(f"Warehouse data saved to {output_path}")
        print(f"Total records in warehouse: {len(merged)}")
        print("--- Warehouse Load Complete ---")
        
    except FileNotFoundError as e:
        print(f"[ERROR] Could not find extracted files. Run extract_sql.py first. Details: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Transformation failed: {e}")
        raise

if __name__ == "__main__":
    transform_and_load_warehouse()
