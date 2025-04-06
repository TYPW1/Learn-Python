# ---- SETUP ----
import os
from openai import OpenAI
from PyPDF2 import PdfReader
import textwrap
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- PDF EXTRACT ----
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text.strip()


pdf_path = "../paper.pdf"  # Update this path
raw_text = extract_text_from_pdf(pdf_path)
print("✅ PDF text extracted.")


# ---- CHUNKING ----
def chunk_text(text, max_words=700):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


chunks = chunk_text(raw_text)
print(f"📄 Split into {len(chunks)} chunks.")


# ---- GPT SUMMARIZATION ----
def summarize_with_gpt(content, model="gpt-3.5-turbo"):
    system_prompt = "You are a helpful assistant that summarizes academic papers clearly and concisely."
    user_prompt = f"Summarize the following academic text:\n\n{content}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


# ---- RUN ON CHUNKS ----
summaries = []
for i, chunk in enumerate(chunks):
    print(f"🧠 Summarizing chunk {i + 1}/{len(chunks)}...")
    summary = summarize_with_gpt(chunk)
    summaries.append(summary)

# ---- FINAL SUMMARY ----
final_summary = "\n\n".join(
    [textwrap.fill(s, width=100) for s in summaries]
)

def save_summary_to_pdf(text, filename="LLM_Summary(gpt).pdf"):
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
            if y < 40:  # Create new page if too low
                c.showPage()
                y = y_margin
            c.drawString(x_margin, y, subline)
            y -= line_height

    c.save()
    print(f"📄 Summary saved as '{filename}'")

# Save final_summary to PDF
save_summary_to_pdf(final_summary)
