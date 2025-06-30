import pandas as pd
import os

def load_excel(file, default_columns):
    if os.path.exists(file):
        return pd.read_excel(file)
    else:
        return pd.DataFrame(columns=default_columns)

def save_excel(df, file):
    df.to_excel(file, index=False)
    
