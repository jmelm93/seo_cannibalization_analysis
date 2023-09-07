import pandas as pd
import time 
from pathlib import Path

def create_excel_file(dict_of_dfs, export_name):
    """
    Create excel file with the dictionary of dfs.
    """
    filename = f"{export_name}_" + str(int(time.time())) + ".xlsx"
    Path("output").mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(f'output/{filename}') as writer:
        for sheet_name, df in dict_of_dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)