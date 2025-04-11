# ocr_utils.py

import fitz  # PyMuPDF
import easyocr
import tempfile
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

def extract_text_from_first_page(pdf_path: str, lang='en') -> str:
    """
    Extracts OCR text from the first page of a scanned PDF.
    
    Args:
        pdf_path (str): Full path to the PDF file.
        lang (str): Language for EasyOCR (default 'en').

    Returns:
        str: The extracted text as a string.
    """
    # Load the first page as an image using PyMuPDF
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    
    # Save page as a temporary image
    pix = page.get_pixmap(dpi=300)
    temp_img = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    pix.save(temp_img.name)

    # OCR using EasyOCR
    reader = easyocr.Reader([lang])
    result = reader.readtext(temp_img.name, detail=0)
    
    # Clean up temp image
    os.unlink(temp_img.name)
    
    return "\n".join(result)


#test and debug the code
path = os.path.join(ABS_PATH, 'sample.pdf')
if not os.path.exists(path):
    raise FileNotFoundError(f"File {path} does not exist.")
print(extract_text_from_first_page(path, lang='en'))