import json
import os

NOTEBOOK_PATH = r"notebooks/visualization_interactive.ipynb"

def add_delivery_stats():
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
            "## 4. Detailed Delivery Analysis\n",
            "Analysis of delivery efficiency by Employee and Country."
        ]
    }

    # Code cell
    code_source = [
        "# Delivery Status Analysis\n",
        "if 'df' in locals():\n",
        "    # 1. Delivery Status by Employee\n",
        "    # Group by LastName and DeliveredFlag\n",
        "    emp_delivery = df.groupby(['LastName', 'DeliveredFlag']).size().reset_index(name='Count')\n",
        "    # Map flag to text\n",
        "    emp_delivery['Status'] = emp_delivery['DeliveredFlag'].map({1: 'Delivered', 0: 'Not Delivered'})\n",
        "    \n",
        "    fig_emp = px.bar(emp_delivery, x='LastName', y='Count', color='Status', \n",
        "                     title='Delivery Status by Employee', \n",
        "                     labels={'LastName': 'Employee', 'Count': 'Number of Orders'},\n",
        "                     barmode='stack')\n",
        "    \n",
        "    # 2. Delivery Status by Country (Customer Country)\n",
        "    # Note: Using Country_x based on previous cells (Customer Country)\n",
        "    country_delivery = df.groupby(['Country_x', 'DeliveredFlag']).size().reset_index(name='Count')\n",
        "    country_delivery['Status'] = country_delivery['DeliveredFlag'].map({1: 'Delivered', 0: 'Not Delivered'})\n",
        "    \n",
        "    fig_country = px.bar(country_delivery, x='Country_x', y='Count', color='Status', \n",
        "                         title='Delivery Status by Country', \n",
        "                         labels={'Country_x': 'Country', 'Count': 'Number of Orders'},\n",
        "                         barmode='stack')\n",
        "    \n",
        "    # Display figures\n",
        "    fig_emp.update_layout(height=500)\n",
        "    fig_country.update_layout(height=500)\n",
        "    \n",
        "    try:\n",
        "        fig_emp.show()\n",
        "        fig_country.show()\n",
        "        fig_emp.write_html(\"../figures/delivery_by_employee.html\")\n",
        "        fig_country.write_html(\"../figures/delivery_by_country.html\")\n",
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
    
    print("Successfully added Delivery Statistics to notebook.")

if __name__ == "__main__":
    add_delivery_stats()
