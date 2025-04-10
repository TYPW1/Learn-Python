import os
import glob
import easyocr
import fitz  # PyMuPDF
from openai import OpenAI
from openpyxl import load_workbook
from dotenv import load_dotenv

# === CONFIG ===
FOLDER_PATH = "./forms"  # Folder containing AVS/DFI PDFs
EXCEL_PATH = "./data_output.xlsm"
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_latest_file(keyword):
    files = glob.glob(os.path.join(FOLDER_PATH, f"*{keyword}*.pdf"))
    return max(files, key=os.path.getmtime) if files else None

def ocr_pdf(file_path):
    reader = easyocr.Reader(['en'], gpu=False)
    text_all = []
    doc = fitz.open(file_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        image_path = f"{file_path}_page{i}.png"
        pix.save(image_path)
        result = reader.readtext(image_path, detail=0)
        text_all.extend(result)
        os.remove(image_path)
    return " ".join(text_all)

# === OCR both AVS and DFI ===
avs_text = ocr_pdf(get_latest_file("AVS")) or ""
dfi_text = ocr_pdf(get_latest_file("DFI")) or ""
combined_text = avs_text + "\n" + dfi_text

# === Ask GPT to extract fields ===
prompt = f"""
Extract the following fields from this form:
1. Full Name
2. Travel destination (city and country code)
3. Start date of travel (e.g., 04 March 2025)

Return in this format:
Name: ...
Travel: ...
Start Date: ...                                         

Text:
{combined_text}
"""

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    output = response.choices[0].message.content
except Exception as e:
    print(f"Error: {e}")
    output = None  # Ensure output is defined even if the API call fails



# === Parse GPT result ===
def extract_value(field, text):
    for line in text.splitlines():
        if line.lower().startswith(field.lower()):
            return line.split(":", 1)[-1].strip()
    return ""

if output:
    # === Parse GPT result ===
    name = extract_value("Name", output)
    travel = extract_value("Travel", output)
    date = extract_value("Start Date", output)

    # === Append to Excel ===
    wb = load_workbook(EXCEL_PATH, keep_vba=True)
    ws = wb.active
    ws.append([name, travel, date])
    wb.save(EXCEL_PATH)

    print("✅ Done! Added row:", name, travel, date)
else:
    print("❌ Failed to get a response from the API. Please check your API key and try again.")
