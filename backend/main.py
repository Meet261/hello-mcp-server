import os
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
import tempfile
import fitz  # PyMuPDF
import google.generativeai as genai

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_url(url):
    resp = requests.get(url)
    if resp.headers.get('content-type', '').startswith('application/pdf'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(resp.content)
            tmp.flush()
            return extract_text_from_pdf(tmp.name)
    else:
        # Fallback: extract text from HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, 'html.parser')
        return soup.get_text()

def summarize_with_gemini(text, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Summarize this research paper:\n{text}")
    return response.text

@app.get("/mcp")
async def mcp_get():
    return {"message": "MCP Summarization Server is running."}

@app.post("/mcp")
async def mcp_post(request: Request, file: UploadFile = File(None), url: str = Form(None), geminiApiKey: str = Form(None)):
    if not geminiApiKey:
        return JSONResponse(status_code=400, content={"error": "Missing Gemini API key."})
    try:
        if file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                tmp.flush()
                text = extract_text_from_pdf(tmp.name)
        elif url:
            text = extract_text_from_url(url)
        else:
            return JSONResponse(status_code=400, content={"error": "No file or URL provided."})
        if not text.strip():
            return JSONResponse(status_code=400, content={"error": "No text extracted from input."})
        summary = summarize_with_gemini(text, geminiApiKey)
        return {"summary": summary}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/mcp")
async def mcp_delete():
    return {"message": "DELETE not implemented, but endpoint is required by Smithery."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port) 