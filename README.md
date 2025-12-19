# ING3 Security Project

## Project Structure
- `/data`: Contains all source Excel files (`Orders.xlsx`, etc.).
- `/scripts`: Contains the project scripts, including the entry point `main.py`.
- `/figures`: Contains generated charts (`orders_by_country.png`, etc.).
- `/reports`: Contains the assignment PDF.
- `/notebooks`: Placeholder for Jupyter notebooks.
- `/video`: Placeholder for the presentation video.

## Setup
1. Install Python dependencies:
   ```bash
   pip install pandas pyodbc openpyxl matplotlib seaborn
   ```
2. Ensure SQL Server is running and accessible at `asus_zakami\SQLAMINE`.

## Execution

You can run the project using either the Python script or the provided Batch file.

### Option 1: Python Script
Run the main pipeline script directly:
```bash
python scripts/main.py
```

### Option 2: Batch File
Double-click `start_pipeline.bat` or run it from the command line:
```bash
start_pipeline.bat
```
Check the `/figures` directory for the output images.
