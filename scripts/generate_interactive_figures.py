import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from settings import DATA_DIR, FIGURES_DIR

# Ensure figures directory exists
os.makedirs(FIGURES_DIR, exist_ok=True)

def load_data():
    data_path = os.path.join(DATA_DIR, "warehouse", "merged_northwind.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Warehouse data not found at {data_path}")
    df = pd.read_csv(data_path)
    df['FullDate'] = pd.to_datetime(df['FullDate'])
    return df

def create_delivery_stats(df):
    """Create interactive pie chart for delivery statistics"""
    delivery_counts = df['DeliveredFlag'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=['Delivered', 'Not Delivered'],
        values=[delivery_counts.get(1, 0), delivery_counts.get(0, 0)],
        hole=0.3,
        marker=dict(colors=['#2ecc71', '#e74c3c']),
        textinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Order Delivery Status',
        font=dict(size=14),
        showlegend=True,
        height=500
    )
    
    save_path = os.path.join(FIGURES_DIR, "delivery_stats_interactive.html")
    fig.write_html(save_path)
    print(f"Saved {save_path}")
    return fig

def create_orders_by_country(df):
    """Create interactive bar chart for orders by country"""
    country_orders = df['Country_x'].value_counts().reset_index()
    country_orders.columns = ['Country', 'OrderCount']
    
    fig = px.bar(
        country_orders,
        x='Country',
        y='OrderCount',
        title='Total Orders by Country',
        color='OrderCount',
        color_continuous_scale='Viridis',
        hover_data={'OrderCount': ':,'}
    )
    
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Number of Orders',
        font=dict(size=12),
        height=600,
        hovermode='x'
    )
    
    save_path = os.path.join(FIGURES_DIR, "orders_by_country_interactive.html")
    fig.write_html(save_path)
    print(f"Saved {save_path}")
    return fig

def create_orders_by_employee(df):
    """Create interactive horizontal bar chart for orders by employee"""
    df['EmployeeName'] = df['FirstName'] + ' ' + df['LastName']
    employee_orders = df['EmployeeName'].value_counts().reset_index()
    employee_orders.columns = ['EmployeeName', 'OrderCount']
    
    fig = px.bar(
        employee_orders,
        y='EmployeeName',
        x='OrderCount',
        orientation='h',
        title='Orders by Employee',
        color='OrderCount',
        color_continuous_scale='Plasma'
    )
    
    fig.update_layout(
        xaxis_title='Number of Orders',
        yaxis_title='Employee',
        font=dict(size=12),
        height=600
    )
    
    save_path = os.path.join(FIGURES_DIR, "orders_by_employee_interactive.html")
    fig.write_html(save_path)
    print(f"Saved {save_path}")
    return fig

def create_monthly_trend(df):
    """Create interactive line chart for monthly trends"""
    df['YearMonth'] = df['FullDate'].dt.to_period('M').astype(str)
    monthly_orders = df.groupby('YearMonth').size().reset_index(name='OrderCount')
    
    fig = px.line(
        monthly_orders,
        x='YearMonth',
        y='OrderCount',
        title='Monthly Orders Trend',
        markers=True
    )
    
    fig.update_traces(
        line=dict(color='#3498db', width=3),
        marker=dict(size=8)
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Orders',
        font=dict(size=12),
        height=600,
        hovermode='x unified'
    )
    
    save_path = os.path.join(FIGURES_DIR, "monthly_trend_interactive.html")
    fig.write_html(save_path)
    print(f"Saved {save_path}")
    return fig

def create_3d_scatter(df):
    """Create interactive 3D scatter plot"""
    df['MonthNum'] = df['FullDate'].dt.month
    agg = df.groupby(['MonthNum', 'Country_x']).size().reset_index(name='OrderCount')
    
    fig = px.scatter_3d(
        agg,
        x='MonthNum',
        y='Country_x',
        z='OrderCount',
        color='OrderCount',
        size='OrderCount',
        title='3D View: Orders by Month and Country',
        color_continuous_scale='Turbo',
        hover_data={'MonthNum': True, 'Country_x': True, 'OrderCount': True}
    )
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Month',
            yaxis_title='Country',
            zaxis_title='Order Count'
        ),
        font=dict(size=12),
        height=700
    )
    
    save_path = os.path.join(FIGURES_DIR, "3d_orders_interactive.html")
    fig.write_html(save_path)
    print(f"Saved {save_path}")
    return fig

def create_delivery_by_country(df):
    """Create stacked bar chart showing delivery status by country"""
    delivery_by_country = df.groupby(['Country_x', 'DeliveredFlag']).size().reset_index(name='Count')
    delivery_by_country['Status'] = delivery_by_country['DeliveredFlag'].map({1: 'Delivered', 0: 'Not Delivered'})
    
    fig = px.bar(
        delivery_by_country,
        x='Country_x',
        y='Count',
        color='Status',
        title='Delivery Status by Country',
        barmode='stack',
        color_discrete_map={'Delivered': '#2ecc71', 'Not Delivered': '#e74c3c'}
    )
    
    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Number of Orders',
        font=dict(size=12),
        height=600
    )
    
    save_path = os.path.join(FIGURES_DIR, "delivery_by_country_interactive.html")
    fig.write_html(save_path)
    print(f"Saved {save_path}")
    return fig

def create_dashboard(df):
    """Create a comprehensive dashboard with multiple charts"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Delivery Status', 'Orders by Country', 'Monthly Trend', 'Top Employees'),
        specs=[[{'type': 'pie'}, {'type': 'bar'}],
               [{'type': 'scatter'}, {'type': 'bar'}]]
    )
    
    # Delivery Status Pie
    delivery_counts = df['DeliveredFlag'].value_counts()
    fig.add_trace(
        go.Pie(labels=['Delivered', 'Not Delivered'],
               values=[delivery_counts.get(1, 0), delivery_counts.get(0, 0)],
               marker=dict(colors=['#2ecc71', '#e74c3c'])),
        row=1, col=1
    )
    
    # Orders by Country
    country_orders = df['Country_x'].value_counts().head(5).reset_index()
    country_orders.columns = ['Country', 'Count']
    fig.add_trace(
        go.Bar(x=country_orders['Country'], y=country_orders['Count'],
               marker=dict(color='#3498db')),
        row=1, col=2
    )
    
    # Monthly Trend
    df['YearMonth'] = df['FullDate'].dt.to_period('M').astype(str)
    monthly = df.groupby('YearMonth').size().reset_index(name='Count')
    fig.add_trace(
        go.Scatter(x=monthly['YearMonth'], y=monthly['Count'],
                   mode='lines+markers', line=dict(color='#9b59b6')),
        row=2, col=1
    )
    
    # Top Employees
    df['EmployeeName'] = df['FirstName'] + ' ' + df['LastName']
    employee_orders = df['EmployeeName'].value_counts().head(5).reset_index()
    employee_orders.columns = ['Employee', 'Count']
    fig.add_trace(
        go.Bar(y=employee_orders['Employee'], x=employee_orders['Count'],
               orientation='h', marker=dict(color='#e67e22')),
        row=2, col=2
    )
    
    fig.update_layout(
        title_text='Northwind Orders Dashboard',
        showlegend=False,
        height=900,
        font=dict(size=10)
    )
    
    save_path = os.path.join(FIGURES_DIR, "dashboard_interactive.html")
    fig.write_html(save_path)
    print(f"Saved {save_path}")
    return fig

if __name__ == "__main__":
    print("--- Generating Interactive Figures ---")
    try:
        df = load_data()
        create_delivery_stats(df)
        create_orders_by_country(df)
        create_orders_by_employee(df)
        create_monthly_trend(df)
        create_3d_scatter(df)
        create_delivery_by_country(df)
        create_dashboard(df)
        print("--- Interactive Figures Generated Successfully ---")
    except Exception as e:
        print(f"[ERROR] Failed to generate figures: {e}")
