import requests
from io import BytesIO
from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)

def download_pdf_content(url: str) -> bytes:
    """
    Downloads PDF content from a given URL.

    Args:
        url (str): The URL of the PDF file.

    Returns:
        bytes: The content of the PDF file as bytes.

    Raises:
        requests.exceptions.RequestException: If the download fails.
    """
    logger.info(f"Attempting to download PDF from: {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        pdf_bytes = response.content
        logger.info(f"Successfully downloaded PDF from {url}. Size: {len(pdf_bytes)} bytes.")
        return pdf_bytes
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download PDF from {url}: {e}")
        raise

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extracts text from PDF content (bytes).

    Args:
        pdf_content (bytes): The raw bytes content of a PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    try:
        # pypdf can read from a BytesIO object directly
        reader = PdfReader(BytesIO(pdf_content))
        for page in reader.pages:
            text += page.extract_text() or "" # Handle pages with no extractable text
        logger.info(f"Successfully extracted text from PDF. Total characters: {len(text)}")
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}", exc_info=True)
        # Depending on severity, you might raise an exception or return empty string
        text = "" # Return empty string if extraction fails
    return text

