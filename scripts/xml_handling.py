from lxml import etree
from typing import Any
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

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
    "PodatekNaliczony": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_43\"]",
    "PodstawaPodatkuNaliczonego": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_42\"]",
    "PodstawaPodatkuNaleznego": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_37\"]",
    "PodatekNalezny": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_38\"]",
    "PodstawaPodatkuNaleznego2": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_19\"]",
    "PodatekNalezny2": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_20\"]",
    "Ewidencja" : "./*[local-name()=\"Ewidencja\"]",
    "SprzedazWiersz": "./*[local-name()=\"Ewidencja\"]/*[local-name()=\"SprzedazWiersz\"]",
    "SprzedazCtrl": "./*[local-name()=\"Ewidencja\"]/*[local-name()=\"SprzedazCtrl\"]",
    "ZakupWiersz": "./*[local-name()=\"Ewidencja\"]/*[local-name()=\"ZakupWiersz\"]",
    "ZakupCtrl": "./*[local-name()=\"Ewidencja\"]/*[local-name()=\"ZakupCtrl\"]",
    "TotalPodatekNaliczony": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_48\"]",
    "DoWplaty": "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_51\"]",
    "NadwyzkaNaliczonego" : "./*[local-name()=\"Deklaracja\"]/*[local-name()=\"PozycjeSzczegolowe\"]/*[local-name()=\"P_53\"]",
}

def D(x): return Decimal(str(x).replace(",", ".") if x is not None else "0")
def q2(x):
    return str(int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP)))



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
        tree.write(xml_filepath, encoding='UTF-8', pretty_print=True, xml_declaration=True)
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
        tree_new.write(xml_filepath, encoding='UTF-8', pretty_print=True, xml_declaration=True)
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

    tree.write(xml_filepath, encoding='UTF-8', pretty_print=True, xml_declaration=True)
    return

def import_sales_data(sales_data: Any, xml_filepath: str) -> None:
    tree = etree.parse(xml_filepath)
    root = tree.getroot()
    xpath_ewidencja = XPATH_MAP.get("Ewidencja")
    ewidencja_list = tree.xpath(xpath_ewidencja)
    ewidencja_parent = ewidencja_list[0]
    sum_of_sales_netto, sum_of_sales_tax = Decimal("0"), Decimal("0")
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
        sum_of_sales_netto += D(row["Kwota_netto"])
        sum_of_sales_tax += D(row["Kwota_podatku"])
        sales_row.tail = "\n    "

    P_37_xpath = XPATH_MAP.get("PodstawaPodatkuNaleznego")
    P_38_xpath = XPATH_MAP.get("PodatekNalezny")
    root.xpath(P_37_xpath)[0].text = q2(sum_of_sales_netto)
    root.xpath(P_38_xpath)[0].text = q2(sum_of_sales_tax)
    summary_sales = etree.SubElement(ewidencja_parent, "SprzedazCtrl")
    etree.SubElement(summary_sales, "LiczbaWierszySprzedazy").text = str(len(sales_data.index))
    etree.SubElement(summary_sales, "PodatekNalezny").text = q2(sum_of_sales_tax)
    manual_indent(root)
    tree.write(xml_filepath, encoding='UTF-8', pretty_print=True, xml_declaration=True)
    return


def import_purchases_data(purchases_data: Any, xml_filepath: str) -> None:
    tree = etree.parse(xml_filepath)
    root = tree.getroot()
    xpath_ewidencja = XPATH_MAP.get("Ewidencja")
    ewidencja_list = tree.xpath(xpath_ewidencja)
    ewidencja_parent = ewidencja_list[0]
    sum_of_purchases_netto, sum_of_purchases_tax = Decimal("0"), Decimal("0")
    for index, row in purchases_data.iterrows():
        sales_row = etree.SubElement(ewidencja_parent, "ZakupWiersz")
        etree.SubElement(sales_row, "LpZakupu").text = str(index+1)
        etree.SubElement(sales_row, "KodKrajuNadaniaTIN").text = str(row["Kraj"])
        etree.SubElement(sales_row, "NrDostawcy").text = str(row["NIP_sprzedawcy"])
        etree.SubElement(sales_row, "NazwaDostawcy").text = str(row["Nazwa_sprzedawcy"])
        etree.SubElement(sales_row, "DowodZakupu").text = str(row["Nr_faktury"])
        etree.SubElement(sales_row, "DataZakupu").text = str(row["Data_faktury"].strftime("%Y-%m-%d"))
        etree.SubElement(sales_row, "K_42").text = str(row["Kwota_netto"]).replace(",", ".")
        etree.SubElement(sales_row, "K_43").text = str(row["Kwota_podatku"]).replace(",", ".")
        sum_of_purchases_netto += D(row["Kwota_netto"])
        sum_of_purchases_tax += D(row["Kwota_podatku"])
        sales_row.tail = "\n    "

    P_43_xpath = XPATH_MAP.get("PodatekNaliczony")
    P_42_xpath = XPATH_MAP.get("PodstawaPodatkuNaliczonego")
    root.xpath(P_42_xpath)[0].text = q2(sum_of_purchases_netto)
    root.xpath(P_43_xpath)[0].text = q2(sum_of_purchases_tax)
    summary_purchases = etree.SubElement(ewidencja_parent, "ZakupCtrl")
    etree.SubElement(summary_purchases, "LiczbaWierszyZakupow").text = str(len(purchases_data.index))
    etree.SubElement(summary_purchases, "PodatekNaliczony").text = q2(sum_of_purchases_tax)
    manual_indent(root)
    tree.write(xml_filepath, encoding='UTF-8', pretty_print=True, xml_declaration=True)
    return

def final_touches(xml_filepath: str) -> None:
    tree = etree.parse(xml_filepath)
    root = tree.getroot()
    P_48_xpath = XPATH_MAP.get("TotalPodatekNaliczony")
    P_39_xpath = XPATH_MAP.get("PodatekNaliczonyNadwyzka")
    P_43_xpath = XPATH_MAP.get("PodatekNaliczony")
    P_37_xpath = XPATH_MAP.get("PodstawaPodatkuNaleznego")
    P_38_xpath = XPATH_MAP.get("PodatekNalezny")
    P_19_xpath = XPATH_MAP.get("PodstawaPodatkuNaleznego2")
    P_20_xpath = XPATH_MAP.get("PodatekNalezny2")
    P_51_xpath = XPATH_MAP.get("DoWplaty")
    P_53_xpath = XPATH_MAP.get("NadwyzkaNaliczonego")
    P_62_xpath = XPATH_MAP.get("PodatekNaliczonyPoprzedni")

    root.xpath(P_48_xpath)[0].text = q2(
        D(root.xpath(P_39_xpath)[0].text) + D(root.xpath(P_43_xpath)[0].text)
    )

    pozycje_xpath = "./*[local-name()='Deklaracja']/*[local-name()='PozycjeSzczegolowe']"
    pozycje_list = root.xpath(pozycje_xpath)
    if pozycje_list:
        pozycje = pozycje_list[0]
        ns = root.nsmap.get(None)
        if not ns:
            tmp = root.xpath(P_37_xpath) or root.xpath(P_38_xpath) or root.xpath(P_39_xpath)
            if tmp:
                ns = etree.QName(tmp[0]).namespace

        if not root.xpath(P_19_xpath) and root.xpath(P_37_xpath):
            p19_new = etree.Element(etree.QName(ns, "P_19"))
            pozycje.append(p19_new)
        if not root.xpath(P_20_xpath) and root.xpath(P_38_xpath):
            p20_new = etree.Element(etree.QName(ns, "P_20"))
            pozycje.append(p20_new)

        if root.xpath(P_19_xpath) and root.xpath(P_37_xpath):
            root.xpath(P_19_xpath)[0].text = q2(D(root.xpath(P_37_xpath)[0].text))
        if root.xpath(P_20_xpath) and root.xpath(P_38_xpath):
            root.xpath(P_20_xpath)[0].text = q2(D(root.xpath(P_38_xpath)[0].text))

        desired = ["P_19","P_20","P_37","P_38","P_39","P_42","P_43","P_48","P_51","P_53","P_62","P_68","P_69"]
        for tag in desired:
            nodes = pozycje.xpath(f"./*[local-name()='{tag}']")
            for n in nodes:
                if n.getparent() is pozycje:
                    pozycje.remove(n)
                    pozycje.append(n)

    if D(root.xpath(P_38_xpath)[0].text) > D(root.xpath(P_48_xpath)[0].text):
        root.xpath(P_51_xpath)[0].text = q2(
            D(root.xpath(P_38_xpath)[0].text) - D(root.xpath(P_48_xpath)[0].text)
        )
        root.xpath(P_53_xpath)[0].text = "0"
        root.xpath(P_62_xpath)[0].text = "0"
    else:
        root.xpath(P_53_xpath)[0].text = q2(
            D(root.xpath(P_48_xpath)[0].text) - D(root.xpath(P_38_xpath)[0].text)
        )
        root.xpath(P_51_xpath)[0].text = "0"
        root.xpath(P_62_xpath)[0].text = root.xpath(P_53_xpath)[0].text

    tree.write(xml_filepath, encoding='UTF-8', pretty_print=True, xml_declaration=True)
    return



'''
jpk_tree = et.parse("misc/test.xml")
root = jpk_tree.getroot()
print(root[1][0][3].text)
'''
