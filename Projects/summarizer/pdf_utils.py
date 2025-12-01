"""
Shared utility functions for PDF processing and summarization.

This module contains common functions used by both BART and GPT summarizers
to eliminate code duplication.
"""

import textwrap
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file.
        
    Returns:
        str: Extracted text from all pages, stripped of leading/trailing whitespace.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text.strip()


def chunk_text(text, max_words=400):
    """
    Split text into chunks of specified word count.
    
    Args:
        text: The text to split into chunks.
        max_words: Maximum number of words per chunk (default: 400).
        
    Returns:
        list: List of text chunks.
    """
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


def save_summary_to_pdf(text, filename="LLM_Summary.pdf"):
    """
    Save text content to a PDF file with proper formatting.
    
    Args:
        text: The text content to save.
        filename: Output PDF filename (default: "LLM_Summary.pdf").
    """
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
