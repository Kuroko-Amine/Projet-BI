import pandas as pd
import os

DATA_DIR = r"data/extracted"

def analyze_dates():
    files_to_check = {
        "Access_Orders.csv": "OrderDate",
        "FactOrders.csv": "OrderDateKey", # need to check how this keys to DimDate
        "DimDate.csv": "DateKey" # or similar
    }

    for filename, date_col in files_to_check.items():
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            print(f"Skipping {filename}: not found.")
            continue
            
        print(f"--- Analyzing {filename} ---")
        try:
            df = pd.read_csv(path)
            print(f"Columns: {df.columns.tolist()}")
            
            # Smart detection of date columns if the specified one isn't found
            found_col = date_col if date_col in df.columns else None
            if not found_col:
                for col in df.columns:
                    if 'date' in col.lower() or 'time' in col.lower():
                        found_col = col
                        break
            
            if found_col:
                print(f"Using date column: {found_col}")
                # Try parsing
                try:
                    df[found_col] = pd.to_datetime(df[found_col], errors='coerce')
                    years = df[found_col].dt.year.value_counts().sort_index()
                    print("Year distribution:")
                    print(years)
                except Exception as e:
                    # If it's an integer key (like DateKey 20060101) using string slicing
                    print("Attempting to parse as string/int keys...")
                    try:
                        df['Year'] = df[found_col].astype(str).str[:4]
                        print("Year distribution (from string):")
                        print(df['Year'].value_counts().sort_index())
                    except Exception as e2:
                        print(f"Could not parse dates: {e2}")

            else:
                print("No date column found.")
                
        except Exception as e:
            print(f"Error reading {filename}: {e}")
        print("\n")

if __name__ == "__main__":
    analyze_dates()
