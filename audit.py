#Bryan Cabrera, Script to pull info from automotive contracts, 6/01/2025

import os
from PyPDF2 import PdfReader
import json #For storing extracted data
import re
from logging_config import setup_logging
from pdf_utils import extract_text_from_pdf, extract_text_with_ocr

#Processes all PDF files in a given folder and extracts their text
def extract_and_store(pdf_folder):
    extracted_data = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            full_path = os.path.join(pdf_folder, filename)
            text = extract_text_from_pdf(full_path)
            extracted_data.append({
                "filename": filename,
                "text": text
            })
    return extracted_data

#Dictionary
FIELDS_TO_EXTRACT = {
    "vin": "VIN",
    "amount_financed": "Amount Financed",
    "monthly_payment": "Monthly Payment",
    "products": "Aftermarket",
    "we_owe": "We-Owe"
}

#Finds and extracts lines from the text that conatin a specific keyword
def extract_lines_by_keyword(text, keyword):
    # This regex matches the keyword anywhere, optional colon/dash, then captures everything after (including tabs/spaces)
    pattern = re.compile(rf"{re.escape(keyword)}\s*[:\-]?\s*([^\n\r]*)", re.IGNORECASE)
    matches = []
    for line in text.splitlines():
        for match in pattern.finditer(line):
            value = match.group(1).strip()
            if value:
                matches.append(value)
    return matches

#Extracts multiple fields from the text using keywords
def extract_all_fields(text):
    results = {}
    for field, keyword in FIELDS_TO_EXTRACT.items():
        results[field] = extract_lines_by_keyword(text, keyword)
    return results

#Normalizes text by replacing whitespace(including newlines) with a single space
def normalize_text(text):
    import re
    return re.sub(r'\s+', ' ', text)

def extract_field(text, keyword):
    import re
    # This will match the keyword, optional colon/dash, then capture the value after it
    pattern = re.compile(rf"{re.escape(keyword)}\s*[:\-]?\s*([^\$,\n]+[\$,\d,\.%]+)", re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return ""

def main():
    setup_logging()
    pdf_folder = "pdfs" #Don't forget to create this folder with sample PDFs
    data = extract_and_store(pdf_folder)

    for item in data:
        print(f"File: {item['filename']}")
        print("----- Extracted Text -----")
        print(repr(item['text']))
        print("--------------------------")
        extracted = extract_all_fields(item['text'])
        for field, values in extracted.items():
            print(f"{field}: {values}")
        normalized = normalize_text(item['text'])
        vin = extract_field(normalized, "VIN")
        amount_financed = extract_field(normalized, "Amount Financed")
        monthly_payment = extract_field(normalized, "Monthly Payment")
        products = extract_field(normalized, "Aftermarket")
        we_owe = extract_field(normalized, "We-Owe")

        print(f"vin: {vin}")
        print(f"amount_financed: {amount_financed}")
        print(f"monthly_payment: {monthly_payment}")
        print(f"products: {products}")
        print(f"we_owe: {we_owe}")

#Runs main() if this file is being run directly
if __name__ == "__main__":
    main()