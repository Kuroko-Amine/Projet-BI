import json
import os

NOTEBOOK_PATH = r"notebooks/visualization_interactive.ipynb"

def add_3d_graph():
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"Notebook not found at {NOTEBOOK_PATH}")
        return

    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Markdown cell
    md_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. OLAP 3D Analysis\n",
            "Visualizing Orders by Customer, Employee, and Date."
        ]
    }

    # Code cell
    code_source = [
        "# OLAP 3D Visualization: Orders by Customer, Employee, Date\n",
        "if 'df' in locals():\n",
        "    # Aggregate data\n",
        "    # Using CompanyName for Customer, LastName for Employee\n",
        "    olap_df = df.groupby(['CompanyName', 'LastName', 'FullDate']).size().reset_index(name='OrderCount')\n",
        "    \n",
        "    # Plotly Express 3D Scatter\n",
        "    fig_3d = px.scatter_3d(\n",
        "        olap_df,\n",
        "        x='CompanyName',\n",
        "        y='LastName',\n",
        "        z='FullDate',\n",
        "        size='OrderCount',\n",
        "        color='OrderCount',\n",
        "        color_continuous_scale='Viridis',\n",
        "        title='OLAP View: Orders by Customer, Employee, Date',\n",
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

    code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code_source
    }

    # Append new cells
    nb['cells'].append(md_cell)
    nb['cells'].append(code_cell)

    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=4)
    
    print("Successfully added 3D graph to notebook.")

if __name__ == "__main__":
    add_3d_graph()
