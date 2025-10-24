#!/usr/bin/env python3
import scripts.xlsx_handling as bxlsx, scripts.xml_handling as bxml

def main() -> None:
    excel_file: str = "Main_Sheet.xlsx"
    xml_file: str = "misc/test2.xml"
    general_info: dict[str, str] = bxlsx.export_company_info(excel_file)
    bxml.apply_company_data(general_info, xml_file)
    bxml.import_previous_tax("misc/test2.xml", xml_file)
    bxml.clean_ewidencja("output.xml")
    bxml.import_sales_data(bxlsx.export_sales_data(excel_file), "output.xml")
    return

if __name__== "__main__":
    main()