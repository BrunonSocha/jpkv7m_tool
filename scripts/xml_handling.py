from lxml import etree
from typing import Any
import pandas as pd

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
    "PodstawaPodatkuNaleznego": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_37\"]",
    "PodatekNalezny": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_38\"]",
    "Ewidencja" : "./*[local-name()=\"Ewidencja\"]",
    "SprzedazWiersz": "./*[local-name()=\"Ewidencja\"]/*[local-name()=\"SprzedazWiersz\"]",
    "SprzedazCtrl": "./*[local-name()=\"Ewidencja\"]/*[local-name()=\"SprzedazCtrl\"]",
    "ZakupWiersz": "./*[local-name()=\"Ewidencja\"]/*[local-name()=\"ZakupWiersz\"]",
    "ZakupCtrl": "./*[local-name()=\"Ewidencja\"]/*[local-name()=\"ZakupCtrl\"]",
}

def manual_indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for subelem in elem:
            manual_indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            subelem.tail = i
    else:
        if not elem.tail or not elem.tail.strip():
            elem.tail = i

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
        tree.write("output.xml", encoding='UTF-8', pretty_print=True, xml_declaration=True)
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
        tree_new.write("output.xml", encoding='UTF-8', pretty_print=True, xml_declaration=True)
    except FileNotFoundError:
        print(f"File not found at {xml_filepath}.")
    except Exception as e:
        print(f"Error: {e}")
    print("Input tax imported.")
    return

def clean_ewidencja(xml_filepath: str) -> None:
    tree = etree.parse(xml_filepath)
    xpath_sale = XPATH_MAP.get("SprzedazWiersz")
    xpath_purchase = XPATH_MAP.get("ZakupWiersz")
    xpath_ewidencja = XPATH_MAP.get("Ewidencja")
    xpath_sale_ctrl = XPATH_MAP.get("SprzedazCtrl")
    xpath_purchase_ctrl = XPATH_MAP.get("ZakupCtrl")
    for ewidencja in tree.xpath(xpath_ewidencja):
        for old_sale in tree.xpath(xpath_sale):
            ewidencja.remove(old_sale)
        for old_purchase in tree.xpath(xpath_purchase):
            ewidencja.remove(old_purchase)
        for sale_ctrl in tree.xpath(xpath_sale_ctrl):
            ewidencja.remove(sale_ctrl)
        for purchase_ctrl in tree.xpath(xpath_purchase_ctrl):
            ewidencja.remove(purchase_ctrl)

    tree.write("output.xml", encoding='UTF-8', pretty_print=True, xml_declaration=True)
    return

def import_sales_data(sales_data: Any, xml_filepath: str) -> None:
    tree = etree.parse(xml_filepath)
    root = tree.getroot()
    xpath_ewidencja = XPATH_MAP.get("Ewidencja")
    ewidencja_list = tree.xpath(xpath_ewidencja)
    ewidencja_parent = ewidencja_list[0]
    sum_of_sales_netto, sum_of_sales_tax = 0, 0
    for index, row in sales_data.iterrows():
        sales_row = etree.SubElement(ewidencja_parent, "SprzedazWiersz")
        etree.SubElement(sales_row, "LpSprzedazy").text = str(index+1)
        etree.SubElement(sales_row, "KodKrajuNadaniaTIN").text = str(row["Kraj"])
        etree.SubElement(sales_row, "NrKontrahenta").text = str(row["NIP_nabywcy"])
        etree.SubElement(sales_row, "NazwaKontrahenta").text = str(row["Nazwa_nabywcy"])
        etree.SubElement(sales_row, "DowodSprzedazy").text = str(row["Nr_faktury"])
        etree.SubElement(sales_row, "DataWystawienia").text = str(row["Data_faktury"].strftime("%Y-%m-%d"))
        etree.SubElement(sales_row, "K_19").text = str(row["Kwota_netto"]).replace(",", ".")
        etree.SubElement(sales_row, "K_20").text = str(row["Kwota_podatku"]).replace(",", ".")
        sum_of_sales_netto += float(str(row["Kwota_podatku"]).replace(",", "."))
        sum_of_sales_tax += float(str(row["Kwota_podatku"]).replace(",", "."))
        sales_row.tail = "\n    "

    P_37_xpath = XPATH_MAP.get("PodstawaPodatkuNaleznego")
    P_38_xpath = XPATH_MAP.get("PodatekNalezny")
    root.xpath(P_37_xpath)[0].text = str(sum_of_sales_netto)
    root.xpath(P_38_xpath)[0].text = str(sum_of_sales_tax)
    summary_sales = etree.SubElement(ewidencja_parent, "SprzedazCtrl")
    etree.SubElement(summary_sales, "LiczbaWierszySprzedazy").text = str(len(sales_data.index))
    etree.SubElement(summary_sales, "PodatekNalezny").text = str(sum_of_sales_tax)
    manual_indent(root)
    tree.write("output.xml", encoding='UTF-8', pretty_print=True, xml_declaration=True)
    return
                      
'''
jpk_tree = et.parse("misc/test.xml")
root = jpk_tree.getroot()
print(root[1][0][3].text)
'''
