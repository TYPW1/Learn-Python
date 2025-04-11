# ocr_utils.py

import fitz  # PyMuPDF
import easyocr
import tempfile
import os
import uuid

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

lang=['en', 'fr']

def extract_text_from_first_page(pdf_path: str) -> str:
    """
    Extracts OCR text from the first page of a scanned PDF.
    
    Args:
        pdf_path (str): Full path to the PDF file.
        lang (list): Languages for EasyOCR (default ['en', 'fr']).

    Returns:
        str: The extracted text as a string.
    """
    # Load the first page as an image using PyMuPDF
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    
    # Generate a unique filename
    temp_img_path = os.path.join(tempfile.gettempdir(), f"page_image_{uuid.uuid4().hex}.png")

    # Save page as a temporary image
    pix = page.get_pixmap(dpi=300)
    pix.save(temp_img_path)

    # OCR using EasyOCR
    reader = easyocr.Reader(lang)
    result = reader.readtext(temp_img_path, detail=0)
    
    # Clean up
    try:
        os.remove(temp_img_path)
    except Exception as e:
        print(f"Warning: could not delete temp image {temp_img_path} - {e}")
    
    return "\n".join(result)


#test and debug the code
path = os.path.join(ABS_PATH, 'sample.pdf')
if not os.path.exists(path):
    raise FileNotFoundError(f"File {path} does not exist.")
print(extract_text_from_first_page(path))