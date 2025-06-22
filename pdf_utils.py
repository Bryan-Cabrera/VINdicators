import logging
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                logging.warning(f"No text found on a page in {file_path}")
        return text
    except Exception as e:
        logging.error(f"Failed to extract text from {file_path}: {e}", exc_info=True)
        return ""

def extract_text_with_ocr(file_path):
    try:
        images = convert_from_path(file_path)
        text = ""
        for i, image in enumerate(images):
            ocr_text = pytesseract.image_to_string(image)
            text += ocr_text
        return text
    except Exception as e:
        logging.error(f"OCR failed for {file_path}: {e}", exc_info=True)
        return ""