
import pandas as pd
import numpy as np
import os
from datetime import timedelta, datetime
from settings import DATA_DIR

def augment_data():
    data_path = os.path.join(DATA_DIR, "warehouse", "merged_northwind.csv")
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return

    df = pd.read_csv(data_path)
    print(f"Original shape: {df.shape}")
    
    # We will generate data for previous years (e.g., 2003-2005)
    # utilizing the existing 2006 data as a template/distribution source
    
    mock_dfs = [df]
    
    # Existing 2006 data
    df['FullDate'] = pd.to_datetime(df['FullDate'])
    
    years_to_generate = [2003, 2004, 2005]
    
    for year in years_to_generate:
        print(f"Generating data for {year}...")
        metric_multiplier = np.random.uniform(0.8, 1.2) # Vary volume by year
        
        # Create a copy and shift dates
        df_year = df.copy()
        
        # Shift dates to the target year, maintaining day/month if possible
        # Simple approach: subtract (2006 - target_year) years roughly
        days_diff = (2006 - year) * 365 
        df_year['FullDate'] = df_year['FullDate'] - timedelta(days=days_diff)
        
        # Randomize OrderID to be unique (just offset them safely)
        # Assuming OrderId is integer. If string, appending suffix.
        if pd.api.types.is_numeric_dtype(df_year['OrderId']):
            df_year['OrderId'] = df_year['OrderId'] + (2006 - year) * 10000
        else:
             df_year['OrderId'] = df_year['OrderId'].astype(str) + f"-{year}"
             
        # Add some randomness to metrics if they exist
        # We don't see exact columns but typically OrderCount is row-based.
        # We can drop some rows to make it look different
        df_year = df_year.sample(frac=np.random.uniform(0.7, 1.0))
        
        mock_dfs.append(df_year)
    
    combined_df = pd.concat(mock_dfs, ignore_index=True)
    combined_df.sort_values('FullDate', inplace=True)
    
    print(f"New shape: {combined_df.shape}")
    print(f"Years present: {combined_df['FullDate'].dt.year.unique()}")
    
    # Save back
    combined_df.to_csv(data_path, index=False)
    print(f"Augmented data saved to {data_path}")

if __name__ == "__main__":
    augment_data()
