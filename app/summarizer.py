
import PyPDF2

def extract_text_from_pdf(path: str) -> str:
    reader = PyPDF2.PdfReader(path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text[:6000]  # Truncate to avoid token limit

def summarize_pdf_file(path: str) -> str:
    import openai
    from dotenv import load_dotenv
    import os

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    text = extract_text_from_pdf(path)
    if not text:
        return "No readable text found in the PDF."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": f"Summarize this academic paper:\n\n{text}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()