from extract_sql import extract_from_sql
from extract_access import extract_from_access
import os
import sys

# Ensure immediate output flushing
sys.stdout.reconfigure(line_buffering=True)

def main():
    print("==========================================")
    print("   STARTING DATA EXTRACTION PIPELINE      ")
    print("==========================================")
    
    try:
        # 1. Extract from SQL Server
        extract_from_sql()
        
        print("\n")
        
        # 2. Extract from Access Database
        extract_from_access()
        
        print("\n")
        print("==========================================")
        print("   ALL EXTRACTIONS COMPLETED SUCCESSFULLY ")
        print("==========================================")
        
    except Exception as e:
        print(f"\n[FATAL ERROR] Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
