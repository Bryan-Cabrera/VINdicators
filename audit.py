#Bryan Cabrera, Script to pull info from automotive contracts, 6/01/2025

import os
from PyPDF2 import PdfReader
import json #For storing extracted data

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

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
    "amount_financed": "AMOUNT FINANCED",
    "monthly_payment": "MONTHLY PAYMENT",
    "products": "PRODUCTS",
    "we_owe": "WE OWE"
}

def  extract_lines_by_keyword(text, keyword):
    if isinstance(text, str):
        lines = text.splitlines()
    elif isinstance(text, list):
        lines = text
    else:
        return None
    return [line.strip() for line in lines if keyword.upper() in line.upper()]


def extract_all_fields(text):
    results = {}
    for field, keyword in FIELDS_TO_EXTRACT.items():
        results[field] = extract_lines_by_keyword(text, keyword)
    return results



def main():
    pdf_folder = "mock_pdfs" #Don't forget to create this folder with sample PDFs
    data = extract_and_store(pdf_folder)

    for item in data:
        print(f"File: {item['filename']}")
        extracted = extract_all_fields(item['text'])
        for field, values in extracted.items():
            print(f"{field}: {values}")

#Runs main() if this file is being run directly
if __name__ == "__main__":
    main()