# ocr_utils.py
from transformers import pipeline
import fitz
import tempfile
import os
import uuid

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

def extract_text_from_first_page(pdf_path: str) -> str:
    """
    Extracts text from the first page of a PDF using LayoutLM.

    Args:
        pdf_path (str): Full path to the PDF file.

    Returns:
        str: The extracted text as a string.
    """
    # Initialize the pipeline
    nlp = pipeline(
        "document-question-answering",
        model="impira/layoutlm-document-qa",
    )

    # Convert PDF to image
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)

    # Save as temporary image
    temp_img_path = os.path.join(tempfile.gettempdir(), f"page_image_{uuid.uuid4().hex}.png")
    pix = page.get_pixmap(dpi=300)
    pix.save(temp_img_path)

    # Extract text using general questions
    questions = [
        "What is the full name?",
        "What are the travel details?",
        "What is the travel date?"
    ]

    results = []
    for question in questions:
        result = nlp(temp_img_path, question)
        if isinstance(result, list):
            result = result[0]
        results.append(result.get('answer', ''))

    # Clean up
    try:
        os.remove(temp_img_path)
    except Exception as e:
        print(f"Warning: could not delete temp image {temp_img_path} - {e}")

    return "\n".join(filter(None, results))
extracted_text = extract_text_from_first_page(os.path.join(ABS_PATH, '../../Data/img.png'))