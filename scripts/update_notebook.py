import json
import os

NOTEBOOK_PATH = r"notebooks/visualization_interactive.ipynb"

def update_notebook():
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"Notebook not found at {NOTEBOOK_PATH}")
        return

    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Find the cell to replace
    found = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            # Check if source contains the target string
            source_code = "".join(cell['source'])
            if "# Load the warehouse data" in source_code:
                print("Found target cell. Updating...")
                
                new_source = [
                    "# Load the extracted data from CSVs\n",
                    "extracted_dir = \"../data/extracted\"\n",
                    "\n",
                    "try:\n",
                    "    fact_orders = pd.read_csv(os.path.join(extracted_dir, \"FactOrders.csv\"))\n",
                    "    dim_customers = pd.read_csv(os.path.join(extracted_dir, \"DimCustomer.csv\"))\n",
                    "    dim_employees = pd.read_csv(os.path.join(extracted_dir, \"DimEmployee.csv\"))\n",
                    "    dim_date = pd.read_csv(os.path.join(extracted_dir, \"DimDate.csv\"))\n",
                    "\n",
                    "    # Merge DataFrames to recreate the analysis dataset\n",
                    "    # 1. Join Orders with Customers\n",
                    "    df = fact_orders.merge(dim_customers, on=\"CustomerId\", how=\"left\")\n",
                    "    \n",
                    "    # 2. Join with Employees (will create _x (Customer) and _y (Employee) suffixes)\n",
                    "    df = df.merge(dim_employees, on=\"EmployeeId\", how=\"left\")\n",
                    "    \n",
                    "    # 3. Join with Date\n",
                    "    df = df.merge(dim_date, on=\"DateId\", how=\"left\")\n",
                    "\n",
                    "    df['FullDate'] = pd.to_datetime(df['FullDate'])\n",
                    "    print(\"Data loaded and merged successfully from new CSVs.\")\n",
                    "    print(f\"Total records: {len(df)}\")\n",
                    "    print(df.head())\n",
                    "\n",
                    "except FileNotFoundError as e:\n",
                    "    print(f\"Error loading data: {e}. Please run the extraction scripts first.\")"
                ]
                
                cell['source'] = new_source
                # Clear outputs since they will be invalid
                cell['outputs'] = []
                cell['execution_count'] = None
                found = True
                break
    
    if found:
        with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=4)
        print("Notebook updated successfully.")
    else:
        print("Target cell not found.")

if __name__ == "__main__":
    update_notebook()
