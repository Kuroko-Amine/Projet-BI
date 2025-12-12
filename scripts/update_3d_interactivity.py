import json
import os

NOTEBOOK_PATH = r"notebooks/visualization_interactive.ipynb"

def update_3d_graph_interactivity():
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"Notebook not found at {NOTEBOOK_PATH}")
        return

    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # New code source with Interactivity (Animation Frame)
    code_source = [
        "# OLAP 3D Visualization: Orders by Customer, Employee, Date (with Year Selection)\n",
        "if 'df' in locals():\n",
        "    # Ensure FullDate is datetime\n",
        "    df['FullDate'] = pd.to_datetime(df['FullDate'])\n",
        "    \n",
        "    # Extract Year for animation/selection\n",
        "    df['Year'] = df['FullDate'].dt.year\n",
        "    \n",
        "    # Filter for valid years if needed (e.g., 1996-2006 as requested, though dataset usually ends earlier - we'll take all available)\n",
        "    # The user mentioned 1996 to 2006. We'll ensure we use what's available.\n",
        "    \n",
        "    # Aggregate data: Group by Year, Customer, Employee, Date\n",
        "    # We need Year in the grouping to use it for animation\n",
        "    olap_df = df.groupby(['Year', 'CompanyName', 'LastName', 'FullDate']).size().reset_index(name='OrderCount')\n",
        "    \n",
        "    # Sort by Year to ensure animation plays correctly\n",
        "    olap_df = olap_df.sort_values('Year')\n",
        "    \n",
        "    # Plotly Express 3D Scatter with Animation Frame\n",
        "    fig_3d = px.scatter_3d(\n",
        "        olap_df,\n",
        "        x='CompanyName',\n",
        "        y='LastName',\n",
        "        z='FullDate',\n",
        "        size='OrderCount',\n",
        "        color='OrderCount',\n",
        "        color_continuous_scale='Viridis',\n",
        "        animation_frame='Year',\n",
        "        animation_group='CompanyName',\n",
        "        title='OLAP View: Orders by Customer, Employee, Date (Yearly Selection)',\n",
        "        labels={'CompanyName': 'Customer', 'LastName': 'Employee', 'FullDate': 'Date'}\n",
        "    )\n",
        "    \n",
        "    fig_3d.update_layout(\n",
        "        scene=dict(\n",
        "            xaxis_title='Customer',\n",
        "            yaxis_title='Employee',\n",
        "            zaxis_title='Date'\n",
        "        ),\n",
        "        height=800,\n",
        "        margin=dict(r=0, l=0, b=0, t=50)\n",
        "    )\n",
        "    \n",
        "    try:\n",
        "        fig_3d.write_html(\"../figures/3d_orders_notebook.html\")\n",
        "        fig_3d.show()\n",
        "    except Exception as e:\n",
        "        print(f\"Error displaying/saving plot: {e}\")"
    ]

    # Find and update the cell
    updated = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            # Check if this is the OLAP cell we created earlier
            source_text = "".join(cell['source'])
            if "OLAP 3D Visualization" in source_text or "px.scatter_3d" in source_text:
                cell['source'] = code_source
                cell['execution_count'] = None
                cell['outputs'] = []
                updated = True
                print("Found and updated 3D graph cell.")
                break
    
    if not updated:
        print("Target cell not found. Appending new cell instead.")
        # Fallback: Append if not found
        code_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code_source
        }
        nb['cells'].append(code_cell)

    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=4)
    
    print("Notebook update complete.")

if __name__ == "__main__":
    update_3d_graph_interactivity()
