import requests
from PyPDF2 import PdfReader
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

from dotenv import load_dotenv
load_dotenv()

# ---- CONFIG ----
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
PDF_PATH = "../paper.pdf"

# ---- PDF EXTRACT ----
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text.strip()

raw_text = extract_text_from_pdf(PDF_PATH)
print("✅ PDF text extracted.")

# ---- CHUNKING ----
def chunk_text(text, max_words=400):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

chunks = chunk_text(raw_text)
print(f"📄 Split into {len(chunks)} chunks.")

# ---- HUGGINGFACE SUMMARIZATION ----
def summarize_with_huggingface(text):
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 150,
            "min_length": 40,
            "do_sample": False
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0]['summary_text']
    else:
        print("❌ Error:", response.status_code, response.text)
        return "Error during summarization."

# ---- RUN ON CHUNKS ----
summaries = []
for i, chunk in enumerate(chunks):
    print(f"🧠 Summarizing chunk {i + 1}/{len(chunks)}...")
    summary = summarize_with_huggingface(chunk)
    summaries.append(summary)

# ---- FINAL SUMMARY ----
final_summary = "\n\n".join(
    [textwrap.fill(s, width=100) for s in summaries]
)

# ---- SAVE TO PDF ----
def save_summary_to_pdf(text, filename="LLM_Summary(bart).pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    x_margin = 40
    y_margin = 720
    line_height = 14

    lines = text.split('\n')
    y = y_margin

    for line in lines:
        wrapped_lines = textwrap.wrap(line, width=90)
        for subline in wrapped_lines:
            if y < 40:
                c.showPage()
                y = y_margin
            c.drawString(x_margin, y, subline)
            y -= line_height

    c.save()
    print(f"📄 Summary saved as '{filename}'")

save_summary_to_pdf(final_summary)
