from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.summarizer import summarize_pdf_file, summarize_pdf_url
from app.utils import download_pdf_from_url
import shutil
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize", response_class=HTMLResponse)
async def summarize(request: Request, pdf: UploadFile = None, url: str = Form("")):
    summary = ""
    if pdf:
        file_path = f"{UPLOAD_DIR}/{pdf.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
        summary = summarize_pdf_file(file_path)
        os.remove(file_path)
    elif url:
        file_path = download_pdf_from_url(url)
        if file_path:
            summary = summarize_pdf_file(file_path)
            os.remove(file_path)
        else:
            summary = "Failed to download the PDF from the given URL."
    else:
        summary = "Please upload a file or provide a URL."

    return templates.TemplateResponse("index.html", {"request": request, "summary": summary})


@app.post("/rpc")
async def handle_rpc(request: Request):
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})

    # 🔒 Lazy-loaded tool list: always respond quickly
    if method == "toolList":
        return JSONResponse({
            "result": [
                {
                    "name": "summarize_pdf",
                    "description": "Summarize a PDF from a given URL using OpenAI.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "A direct link to a PDF file"}
                        },
                        "required": ["url"]
                    }
                }
            ]
        })

    # Only initialize heavy dependencies when method is actually called
    if method == "summarize_pdf":
        url = params.get("url")
        if not url:
            return JSONResponse({"error": "Missing 'url'"}, status_code=400)

        # Download and summarize
        path = download_pdf_from_url(url)
        if not path:
            return JSONResponse({"error": "Failed to download PDF"}, status_code=400)

        summary = summarize_pdf_file(path)
        try:
            os.remove(path)
        except Exception:
            pass

        return JSONResponse({"result": summary})

    return JSONResponse({"error": f"Unknown method '{method}'"}, status_code=404)
