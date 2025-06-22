import logging

def setup_logging():
    logging.basicConfig(
        filename='pdf_extraction.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )