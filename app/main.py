import os
from dotenv import load_dotenv # Keep this import here and load_dotenv() call

# Load environment variables FIRST before importing other modules that might use os.getenv
# This ensures GEMINI_API_KEY is available when summarizer.py is imported
load_dotenv() 

from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.summarizer import get_summary # This import now happens AFTER load_dotenv()
from app.utils import extract_text_from_pdf, download_pdf_content
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates for HTML files
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main HTML page for the summarizer UI."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize")
async def summarize_paper_endpoint(
    pdf_file: UploadFile = File(None),
    pdf_url: str = Form(None)
):
    """
    Handles PDF summarization requests.
    Expects either a PDF file upload or a PDF URL.
    """
    pdf_text = ""
    file_source = ""

    try:
        if pdf_file and pdf_file.filename != '':
            logger.info(f"Received file upload: {pdf_file.filename}")
            file_content = await pdf_file.read()
            pdf_text = extract_text_from_pdf(file_content)
            file_source = f"uploaded file: {pdf_file.filename}"
        elif pdf_url:
            logger.info(f"Received PDF URL: {pdf_url}")
            pdf_content_bytes = download_pdf_content(pdf_url)
            pdf_text = extract_text_from_pdf(pdf_content_bytes)
            file_source = f"URL: {pdf_url}"
        else:
            raise HTTPException(status_code=400, detail="No PDF file or URL provided.")

        if not pdf_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract any text from the PDF. It might be an image-only PDF or corrupted.")

        logger.info(f"Extracted text successfully from {file_source}. Length: {len(pdf_text)} characters.")

        # Call the summarizer logic
        summary = get_summary(pdf_text)

        logger.info(f"Summary generated successfully for {file_source}.")
        return {"summary": summary}

    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}", exc_info=True)
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred during summarization: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred during summarization: {e}")

