import requests
from io import BytesIO
from pypdf import PdfReader

def download_pdf(url: str) -> bytes:
    """Download PDF from URL"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def extract_text(pdf_content: bytes) -> str:
    """Extract text from PDF bytes"""
    reader = PdfReader(BytesIO(pdf_content))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text