from scripts.xlsx_handling import import_company_info
from scripts.xml_handling import apply_company_data

def main() -> None:
    excel_file: str = "Main_Sheet.xlsx"
    xml_file: str = "misc/test.xml"
    general_info: dict[str, str] = import_company_info(excel_file)
    apply_company_data(general_info, xml_file)
    return

if __name__== "__main__":
    main()