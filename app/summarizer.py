import PyPDF2
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(path: str) -> str:
    reader = PyPDF2.PdfReader(path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text[:6000]  # Truncate if too long

def summarize_pdf_file(path: str) -> str:
    text = extract_text_from_pdf(path)
    if not text:
        return "No readable text found in the PDF."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-4
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": f"Summarize this academic paper:\n\n{text}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def summarize_pdf_url(url: str) -> str:
    # Optional if you want direct URL-based summarization
    raise NotImplementedError("Use download + summarize instead.")
