from ocr_utils import extract_text_from_first_page
from mistralai_formatter import format_ocr_text_to_json

if __name__ == "__main__":
    # Example PDF path (replace with your actual PDF file path)
    pdf_path = "sample.pdf"
    
    # Extract text from the first page of the PDF
    extracted_text = extract_text_from_first_page(pdf_path, lang='en')
    
    # Format the extracted text to JSON using Mistral AI
    formatted_json = format_ocr_text_to_json(extracted_text)
    
    # Print the formatted JSON output
    print(formatted_json)