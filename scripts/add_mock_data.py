import json
import os

NOTEBOOK_PATH = r"notebooks/visualization_interactive.ipynb"

def inject_mock_data():
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"Notebook not found at {NOTEBOOK_PATH}")
        return

    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Code to generate mock data
    mock_data_source = [
        "# --- MOCK DATA GENERATION (1996-2005) ---\n",
        "# The source data only contains 2006. We generate mock history for visualization purposes.\n",
        "import numpy as np\n",
        "\n",
        "if 'df' in locals():\n",
        "    print(\"Generating mock historical data (1996-2005)...\")\n",
        "    \n",
        "    # Get existing unique entities to maintain referential consistency\n",
        "    customers = df['CompanyName'].unique()\n",
        "    employees = df['LastName'].unique()\n",
        "    \n",
        "    mock_rows = []\n",
        "    # Generate ~500 mock orders scattered across the years\n",
        "    for _ in range(500):\n",
        "        # Random Year between 1996 and 2005\n",
        "        year = np.random.randint(1996, 2006)\n",
        "        # Random Month and Day\n",
        "        month = np.random.randint(1, 13)\n",
        "        day = np.random.randint(1, 28)\n",
        "        mock_date = pd.Timestamp(year=year, month=month, day=day)\n",
        "        \n",
        "        row = {\n",
        "            'CompanyName': np.random.choice(customers),\n",
        "            'LastName': np.random.choice(employees),\n",
        "            'FullDate': mock_date,\n",
        "            'Year': year,\n",
        "            'OrderCount': 1, # Placeholder\n",
        "            'DeliveredFlag': np.random.choice([0, 1]), # Add this for delivery stats\n",
        "            'Country_x': 'USA' # Default mock country to avoid NaN in country stats\n",
        "        }\n",
        "        mock_rows.append(row)\n",
        "    \n",
        "    mock_df = pd.DataFrame(mock_rows)\n",
        "    \n",
        "    # Ensure original df has 'Year' computed if not already\n",
        "    if 'Year' not in df.columns:\n",
        "        df['FullDate'] = pd.to_datetime(df['FullDate'])\n",
        "        df['Year'] = df['FullDate'].dt.year\n",
        "    \n",
        "    # FIXED LINE: Do not subset df. Concatenate everything. \n",
        "    # Mock data will have NaNs for columns we didn't mock, which is fine.\n",
        "    df = pd.concat([df, mock_df], ignore_index=True)\n",
        "    \n",
        "    print(f\"Added {len(mock_df)} mock records. Total records: {len(df)}\")\n"
    ]

    mock_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": mock_data_source
    }

    # Filter out OLD mock cells to avoid duplication if running multiple times
    cleaned_cells = []
    for cell in nb['cells']:
        source = "".join(cell.get('source', []))
        if "MOCK DATA GENERATION" in source and "1996-2005" in source:
             continue # Skip old version
        cleaned_cells.append(cell)
    
    # Insert this cell BEFORE the 3D OLAP cell
    final_cells = []
    found_viz_cell = False
    
    for cell in cleaned_cells:
        source_text = "".join(cell.get('source', []))
        # Look for the cell we added previously
        if "OLAP 3D Visualization" in source_text or "px.scatter_3d" in source_text:
            if not found_viz_cell:
                final_cells.append(mock_cell)
                found_viz_cell = True
        final_cells.append(cell)
    
    if not found_viz_cell:
        final_cells.append(mock_cell)

    nb['cells'] = final_cells

    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=4)
    
    print("Injected (and fixed) mock data generation logic into notebook.")

if __name__ == "__main__":
    inject_mock_data()
