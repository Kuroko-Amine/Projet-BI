import json

notebook_path = "notebooks/visualization_interactive.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell.get('source', []))
        print(f"--- Cell {i} ---")
        print(source)
        print("----------------")
