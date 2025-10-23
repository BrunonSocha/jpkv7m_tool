from lxml import etree
from typing import Any

XPATH_MAP: dict[str, str] = {
    "KodUrzedu": "./*[local-name()=\"Naglowek\"]/*[local-name()=\"KodUrzedu\"]",
    "Rok": "./*[local-name()=\"Naglowek\"]/*[local-name()=\"Rok\"]",
    "Miesiac": "./*[local-name()=\"Naglowek\"]/*[local-name()=\"Miesiac\"]",
    "NIP": "./*[local-name()=\"Podmiot1\"]/*[local-name()=\"OsobaNiefizyczna\"]/*[local-name()=\"NIP\"]",
    "PelnaNazwa": "./*[local-name()=\"Podmiot1\"]/*[local-name()=\"OsobaNiefizyczna\"]/*[local-name()=\"PelnaNazwa\"]",
    "Email": "./*[local-name()=\"Podmiot1\"]/*[local-name()=\"OsobaNiefizyczna\"]/*[local-name()=\"Email\"]",
    "Telefon": "./*[local-name()=\"Podmiot1\"]/*[local-name()=\"OsobaNiefizyczna\"]/*[local-name()=\"Telefon\"]",
    "PodatekNaliczonyPoprzedni": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_62\"]",
    "PodatekNaliczonyNadwyzka": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_39\"]",
}


def apply_company_data(company_data: dict[str, str], xml_filepath: str) -> None:
    etree.register_namespace("etd", "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2021/06/08/eD/DefinicjeTypy/")
    etree.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    try:
        tree = etree.parse(xml_filepath)
        root = tree.getroot()
        for k, v in company_data.items():
            xpath = XPATH_MAP.get(k)
            element_list = root.xpath(xpath)
            element = element_list[0] if element_list else None
            if element is not None:
                element.text = v
            else:
                print("One of the elements was not found.")
        tree.write("output.xml")
    except FileNotFoundError:
        print(f"File not found at {xml_filepath}.")
    except Exception as e:
        print(f"Error: {e}")
    print("Company data applied to the file.")
    return

def import_previous_tax(previous_xml_filepath: str, xml_filepath: str) -> None:
    try:
        tree_old = etree.parse(previous_xml_filepath)
        tree_new = etree.parse(xml_filepath)
        root_old = tree_old.getroot()
        root_new = tree_new.getroot()
        P_62_xpath = XPATH_MAP.get("PodatekNaliczonyPoprzedni")
        P_39_xpath = XPATH_MAP.get("PodatekNaliczonyNadwyzka")
        root_new.xpath(P_39_xpath)[0].text = root_old.xpath(P_62_xpath)[0].text
        tree_new.write("output.xml")
    except FileNotFoundError:
        print(f"File not found at {xml_filepath}.")
    except Exception as e:
        print(f"Error: {e}")
    print("Input tax imported.")
    return
'''
jpk_tree = et.parse("misc/test.xml")
root = jpk_tree.getroot()
print(root[1][0][3].text)
'''
