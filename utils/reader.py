import pandas as pd
import os

def read_csv_auto(filepath: str) -> pd.DataFrame:
    delimiters = [",", ";", "."]
    for delim in delimiters:
        try:
            df = pd.read_csv(filepath, delimiter=delim)
            if df.shape[1] > 1:
                return df
        except Exception:
            continue
    raise ValueError(f"No se pudo leer correctamente: {filepath}")

def list_csv_files(folder="data"):
    return [f for f in os.listdir(folder) if f.endswith(".csv")]
