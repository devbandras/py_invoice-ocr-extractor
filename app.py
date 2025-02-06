import argparse
import json
import re
import pytesseract
from PIL import Image

# Állítsd be a Tesseract elérési útját, ha szükséges
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_tax_number(text):    
    # Adószám mintázatok definiálása
    pattern1 = r'\b\d{8}-\d-\d{2}\b'  # Eredeti adószám mintázat
    pattern2 = r'\b\d{11}\b'          # 11 jegyű szám mintázat

    # Keresés az első mintázatra
    matches1 = re.findall(pattern1, text)
    if matches1:
        return matches1[0]  # Az első találatot adjuk vissza

    # Keresés a második mintázatra
    matches2 = re.findall(pattern2, text)
    if matches2:
        return matches2[0]  # Az első találatot adjuk vissza

    return None  # Ha nincs érvényes adószám

import re

def extract_invoice_number(text):
    # Eltávolítjuk a "bankszámlaszám" szót a szövegből
    text = re.sub(r'bankszámlaszám', '', text, flags=re.IGNORECASE)
    
    # Minden előfordulást megkeresünk
    keywords = [
        "sorszám", "bizonylatszám", "számlaszám",
        "számla száma", "bizonylat száma", "számla sorszáma",
    ]
    
    pattern = r'(?i)(' + '|'.join(keywords) + r'):\s*([A-Za-z0-9/-]+)'
    matches = re.findall(pattern, text)
    
    # Összegyűjtjük az összes talált számlaszámot
    invoice_numbers = []
    for match in matches:
        value = match[1].strip()
        invoice_numbers.append(value)
    
    # Visszaadjuk az összes számlaszámot tartalmazó listát
    return invoice_numbers

def extract_bank_account_number(text):
    # Bankszámlaszám mintázatának definiálása (2x8 vagy 3x8)
    pattern_2x8 = r'\b\d{8}-\d{8}\b'  # 2x8
    pattern_3x8 = r'\b\d{8}-\d{8}-\d{8}\b'  # 3x8

    # Keresés a 3x8-as mintázatra
    matches_3x8 = re.findall(pattern_3x8, text)
    if matches_3x8:
        return matches_3x8[0]  # Az első találatot adjuk vissza
    
    # Keresés a 2x8-as mintázatra
    matches_2x8 = re.findall(pattern_2x8, text)
    if matches_2x8:
        return matches_2x8[0]  # Az első találatot adjuk vissza  

    return None  # Ha nincs érvényes bankszámlaszám

def extract_text_from_image(image_path):
    # Kép betöltése
    image = Image.open(image_path)
    
    # Szöveg kinyerése a képből magyar nyelven
    pytesseract.image_to_boxes(image, lang='hun')
    text = pytesseract.image_to_string(image, lang='hun')
    
    # Adószám kinyerése
    tax_number = extract_tax_number(text)
    
    # Számlaszám kinyerése
    invoice_number = extract_invoice_number(text)
    
    # Bankszámlaszám kinyerése
    bank_account_number = extract_bank_account_number(text)
    
    # JSON formátumú kimenet létrehozása
    output = {
        "raw_text": text,
        "tax_number": tax_number,
        "invoice_number": invoice_number,
        "bank_account_number": bank_account_number
    }
    
    return json.dumps(output, ensure_ascii=False, indent=4)

def extract_bank_account_number_1(text):
    # Bankszámlaszám mintázatának definiálása (2x8 vagy 3x8)
    pattern = r'(?i)bankszámlaszám:\s*([\d-]+(?:-\d{8})?)'
    matches = re.findall(pattern, text)
    
    # Az első találatot adjuk vissza, ha van
    return matches[0] if matches else None


if __name__ == "__main__":
     # Argumentumok kezelése
    parser = argparse.ArgumentParser(description='Kép feldolgozása számlákhoz.')
    parser.add_argument('-invoice', type=str, required=True, help='A számla képe (pl. 01.jpg)')
    args = parser.parse_args()

    # Kép elérési útjának megadása
    image_path = args.invoice
    extracted_text_json = extract_text_from_image(image_path)
    print("Kinyert szöveg JSON formátumban:")
    print(extracted_text_json)
