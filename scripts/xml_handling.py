import xml.etree.ElementTree as et

def apply_company_data(company_data: dict[str, str], xml_filepath: str) -> None:
    jpk_tree = et.parse(xml_filepath)
    et.register_namespace("", "http://crd.gov.pl/wzor/2021/12/27/11148/")
    et.register_namespace("etd", "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2021/06/08/eD/DefinicjeTypy/")
    et.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    jpk_root = jpk_tree.getroot()
    jpk_root[0][5].text = company_data["Kod_urzedu"]
    jpk_root[0][6].text = company_data["Rok"]
    jpk_root[0][7].text = company_data["Miesiac"]
    jpk_root[1][0][0].text = company_data["NIP"]
    jpk_root[1][0][1].text = company_data["Nazwa"]
    jpk_root[1][0][2].text = company_data["Email"]
    jpk_root[1][0][3].text = company_data["Nr_tel"].replace(" ", "").replace("-", "")
    jpk_tree.write("output.xml")
    return

'''
jpk_tree = et.parse("misc/test.xml")
root = jpk_tree.getroot()
print(root[1][0][3].text)
'''
