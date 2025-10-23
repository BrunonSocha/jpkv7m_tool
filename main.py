#!/usr/bin/env python3
from scripts.xlsx_handling import export_company_info
from scripts.xml_handling import apply_company_data, import_previous_tax

def main() -> None:
    excel_file: str = "Main_Sheet.xlsx"
    xml_file: str = "misc/test.xml"
    general_info: dict[str, str] = export_company_info(excel_file)
    apply_company_data(general_info, xml_file)
    import_previous_tax("misc/test2.xml", xml_file)
    return

if __name__== "__main__":
    main()