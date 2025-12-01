import requests
import textwrap
import os

from dotenv import load_dotenv

from pdf_utils import extract_text_from_pdf, chunk_text, save_summary_to_pdf

load_dotenv()

# ---- CONFIG ----
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
PDF_PATH = "../../Data/paper.pdf"

# ---- PDF EXTRACT ----
raw_text = extract_text_from_pdf(PDF_PATH)
print("✅ PDF text extracted.")

# ---- CHUNKING ----
chunks = chunk_text(raw_text, max_words=400)
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
save_summary_to_pdf(final_summary, filename="LLM_Summary(bart).pdf")
