
import nbformat
import os

# Define the new aesthetic content (Run 2: Purple/Teal + Horizontal)
THEME_SETUP = """
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import os

# Ensure figures dir exists
os.makedirs("../figures", exist_ok=True)

# --- Global Design Settings ---
# Set default template
pio.templates.default = "plotly_white"

# Define Custom Color Palette (Modern Tech Theme)
COLORS = {
    'primary': '#6c5ce7',    # Deep Purple
    'secondary': '#00cec9',  # Robinson Teal
    'accent': '#fdcb6e',     # Warm Yellow
    'delivered': '#6c5ce7',  # Purple for Delivered
    'not_delivered': '#00cec9', # Teal for Not Delivered
    'background': '#ffffff', 
    'text': '#2d3436'
}
"""

PIE_CHART_CODE = """if 'df' in locals():
    delivery_counts = df['DeliveredFlag'].value_counts()
    
    # Create Donut Chart with Pulled Slices
    fig = go.Figure(data=[go.Pie(
        labels=['Delivered', 'Not Delivered'],
        values=[delivery_counts.get(1, 0), delivery_counts.get(0, 0)],
        hole=0.4, 
        pull=[0, 0.1], # Pull the 'Not Delivered' slice slightly
        marker=dict(colors=[COLORS['delivered'], COLORS['not_delivered']]), 
        textinfo='label+percent',
        rotation=90
    )])
    
    fig.update_layout(
        title=dict(text='Order Delivery Status', x=0.5, xanchor='center'),
        font=dict(size=14, family="Segoe UI, sans-serif"),
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    try:
        fig.write_html("../figures/delivery_stats_notebook.html")
        fig.show()
    except Exception as e:
        print(f"Error displaying/saving plot: {e}")
"""

# CHANGED: Switched to Horizontal Bar Charts (x/y swapped, orientation='h')
BAR_CHARTS_CODE = """# Delivery Status Analysis
if 'df' in locals():
    # 1. Delivery Status by Employee (Horizontal)
    emp_delivery = df.groupby(['LastName', 'DeliveredFlag']).size().reset_index(name='Count')
    emp_delivery['Status'] = emp_delivery['DeliveredFlag'].map({1: 'Delivered', 0: 'Not Delivered'})
    
    # Note: swapped x and y, and mapping colors
    fig_emp = px.bar(emp_delivery, y='LastName', x='Count', color='Status', 
                     title='Delivery Status by Employee', 
                     orientation='h', # Horizontal
                     labels={'LastName': 'Employee', 'Count': 'Number of Orders'},
                     barmode='stack',
                     color_discrete_map={'Delivered': COLORS['delivered'], 'Not Delivered': COLORS['not_delivered']})
    
    # 2. Delivery Status by Country (Horizontal)
    country_delivery = df.groupby(['Country_x', 'DeliveredFlag']).size().reset_index(name='Count')
    country_delivery['Status'] = country_delivery['DeliveredFlag'].map({1: 'Delivered', 0: 'Not Delivered'})
    
    fig_country = px.bar(country_delivery, y='Country_x', x='Count', color='Status', 
                         title='Delivery Status by Country', 
                         orientation='h', # Horizontal
                         labels={'Country_x': 'Country', 'Count': 'Number of Orders'},
                         barmode='stack',
                         color_discrete_map={'Delivered': COLORS['delivered'], 'Not Delivered': COLORS['not_delivered']})
    
    # Display figures
    for fig in [fig_emp, fig_country]:
        fig.update_layout(
            height=500,
            font=dict(family="Segoe UI, sans-serif"),
            title=dict(x=0.5, xanchor='center'),
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis={'categoryorder':'total ascending'} # Sort bars
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=False)
    
    try:
        fig_emp.show()
        fig_country.show()
        fig_emp.write_html("../figures/delivery_by_employee.html")
        fig_country.write_html("../figures/delivery_by_country.html")
    except Exception as e:
        print(f"Error displaying/saving plot: {e}")
"""

# 3D Code remains unchanged (Plasma) as requested by User
THREED_CHART_CODE = """# OLAP 3D Visualization: Orders by Customer, Employee, Date (with Year Selection)
if 'df' in locals():
    # Ensure FullDate is datetime
    df['FullDate'] = pd.to_datetime(df['FullDate'])
    
    # Extract Year for animation/selection
    df['Year'] = df['FullDate'].dt.year
    
    # Aggregate data: Group by Year, Customer, Employee, Date
    olap_df = df.groupby(['Year', 'CompanyName', 'LastName', 'FullDate']).size().reset_index(name='OrderCount')
    olap_df = olap_df.sort_values('Year')
    
    # Plotly Express 3D Scatter with Animation Frame
    fig_3d = px.scatter_3d(
        olap_df,
        x='CompanyName',
        y='LastName',
        z='FullDate',
        size='OrderCount',
        color='OrderCount',
        color_continuous_scale='Plasma', # Keep Plasma
        animation_frame='Year',
        animation_group='CompanyName',
        title='OLAP View: Orders by Customer, Employee, Date (Yearly Selection)',
        labels={'CompanyName': 'Customer', 'LastName': 'Employee', 'FullDate': 'Date'}
    )
    
    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Customer',
            yaxis_title='Employee',
            zaxis_title='Date',
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor='lightgray'),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor='lightgray'),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor='lightgray'),
        ),
        font=dict(family="Segoe UI, sans-serif"),
        title=dict(x=0.5, xanchor='center'),
        height=800,
        margin=dict(r=0, l=0, b=0, t=50)
    )
    
    try:
        fig_3d.write_html("../figures/3d_orders_notebook.html")
        fig_3d.show()
    except Exception as e:
        print(f"Error displaying/saving plot: {e}")
"""

# Trend Chart Code (Area Chart)
TREND_CHART_CODE = """if 'df' in locals():
    # Create YearMonth column for grouping
    df['YearMonth'] = df['FullDate'].dt.to_period('M').astype(str)
    
    # 4. Monthly Order Trend
    monthly_trend = df.groupby('YearMonth').size().reset_index(name='Count')
    monthly_trend = monthly_trend.sort_values('YearMonth')
    
    # Area Chart for Trend
    fig = px.area(monthly_trend, x='YearMonth', y='Count', 
                  title='Monthly Order Trend',
                  markers=True,
                  labels={'YearMonth': 'Month', 'Count': 'Number of Orders'})
    
    fig.update_traces(line_color=COLORS['primary'], fill='tozeroy')
    
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif"),
        title=dict(x=0.5, xanchor='center'),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='LightGray')
    )
    
    try:
        fig.write_html("../figures/monthly_trend_notebook.html")
        fig.show()
    except Exception as e:
        print(f"Error displaying/saving plot: {e}")
"""

def main():
    nb_path = "../notebooks/visualization_interactive.ipynb"
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    updated_cells = 0
    
    for cell in nb.cells:
        if cell.cell_type == 'code':
            source = cell.source
            
            # Update Imports (Look for previous Theme Setup or standard imports)
            if "import plotly.graph_objects as go" in source:
                print("Updating Imports/Theme cell...")
                cell.source = THEME_SETUP
                updated_cells += 1
                
            # Update Pie Chart
            elif "go.Pie" in source and "DeliveredFlag" in source:
                print("Updating Pie Chart cell...")
                cell.source = PIE_CHART_CODE
                updated_cells += 1
                
            # Update Bar Charts (Delivery Status) - Look for key phrases
            elif "title='Delivery Status by Employee'" in source:
                print("Updating Bar Charts cell...")
                cell.source = BAR_CHARTS_CODE
                updated_cells += 1

            # Update 3D Graph (Ensure strict consistency)
            elif "scatter_3d" in source or "Scatter3d" in source:
                print("Updating/Verifying 3D Graph cell...")
                cell.source = THREED_CHART_CODE
                updated_cells += 1

            # Update Monthly Trend
            elif "YearMonth" in source and "monthly" in source.lower():
                print("Updating Monthly Trend cell...")
                cell.source = TREND_CHART_CODE
                updated_cells += 1


    print(f"Updated {updated_cells} cells.")
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Notebook saved.")

if __name__ == "__main__":
    main()
