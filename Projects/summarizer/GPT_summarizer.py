# ---- SETUP ----
import os
import textwrap
from openai import OpenAI
from dotenv import load_dotenv

from pdf_utils import extract_text_from_pdf, chunk_text, save_summary_to_pdf


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- PDF EXTRACT ----
pdf_path = "../../Data/paper.pdf"  # Update this path
raw_text = extract_text_from_pdf(pdf_path)
print("✅ PDF text extracted.")


# ---- CHUNKING ----
chunks = chunk_text(raw_text, max_words=700)
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

# Save final_summary to PDF
save_summary_to_pdf(final_summary, filename="LLM_Summary(gpt).pdf")
