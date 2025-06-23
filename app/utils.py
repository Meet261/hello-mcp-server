import requests
import uuid
import os

DOWNLOAD_DIR = "downloaded"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_pdf_from_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.headers.get("Content-Type", "").startswith("application/pdf"):
            filename = f"{DOWNLOAD_DIR}/{uuid.uuid4().hex}.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            return None
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None