from ocr_utils import extract_text_from_first_page, ABS_PATH
from mistral import format_ocr_text_to_json
import os

if __name__ == "__main__":
    path = os.path.join(ABS_PATH, 'sample.pdf')
    
    # Extract text from the first page of the PDF
    extracted_text = extract_text_from_first_page(path)
    
    # Format the extracted text to JSON using Mistral AI
    formatted_json = format_ocr_text_to_json(extracted_text)
    
    # Print the formatted JSON output
    print(formatted_json)