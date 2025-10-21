import pandas as pd
from typing import Any 

def import_company_info(file: str) -> dict[str, str]:
    raw_dict: dict[Any, Any] = pd.read_excel(file, usecols=["Kod_urzedu", "Miesiac", "Rok", "NIP", "Nazwa", "Email", "Nr_tel"]).to_dict()
    clean_dict: dict[str, str] = {}
    for k, v in raw_dict.items():
        clean_dict[k] = str(list(v.values())[0])
    return clean_dict

