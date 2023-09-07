import pandas as pd
import time 
from pathlib import Path

def create_excel_file(dict_of_dfs):
    """
    Create excel file with the dictionary of dfs.
    """
    filename = "output_" + str(int(time.time())) + ".xlsx"
    Path("data").mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(f'data/{filename}') as writer:
        for sheet_name, df in dict_of_dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)