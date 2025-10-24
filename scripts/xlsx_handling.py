import pandas as pd
from typing import Any 

def export_company_info(file: str) -> dict[str, str]:
    df = pd.read_excel(file, usecols=["KodUrzedu", "Miesiac", "Rok", "NIP", "PelnaNazwa", "Email", "Telefon"]).to_dict()
    clean_dict = {}
    for k, v in df.items():
        clean_dict[k] = str(list(v.values())[0])
    return clean_dict

def export_sales_data(file: str) -> Any:
    df = pd.read_excel(file, sheet_name=1)
    return df

def export_purchases_data(file: str) -> Any:
    df = pd.read_excel(file, sheet_name=2)
    return df
