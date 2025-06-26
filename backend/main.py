import os
import logging
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
import tempfile
import fitz  # PyMuPDF
import google.generativeai as genai

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.get("/")
async def root():
    logger.info("Health check: / endpoint called.")
    return {"status": "ok"}

@app.get("/mcp")
async def mcp_get():
    logger.info("GET /mcp called for tool discovery.")
    return {
        "message": "MCP Summarization Server is running.",
        "tools": [
            {
                "name": "summarize",
                "description": "Summarize a research paper from PDF or URL using Gemini."
            }
        ]
    }

@app.post("/mcp")
async def mcp_post(request: Request, file: UploadFile = File(None), url: str = Form(None), geminiApiKey: str = Form(None)):
    logger.info("POST /mcp called.")
    if not geminiApiKey:
        logger.error("Missing Gemini API key.")
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
            logger.error("No file or URL provided.")
            return JSONResponse(status_code=400, content={"error": "No file or URL provided."})
        if not text.strip():
            logger.error("No text extracted from input.")
            return JSONResponse(status_code=400, content={"error": "No text extracted from input."})
        summary = summarize_with_gemini(text, geminiApiKey)
        logger.info("Summarization successful.")
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error in POST /mcp: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.delete("/mcp")
async def mcp_delete():
    logger.info("DELETE /mcp called.")
    return {"message": "DELETE not implemented, but endpoint is required by Smithery."}

# MCP server URL (replace with your actual deployment URL)
MCP_SERVER_URL = "https://server.smithery.ai/@smithery-ai/github/mcp"

# If authentication is required, add headers or params as needed
HEADERS = {
    "Authorization": "Bearer YOUR_SMITHERY_API_KEY",  # If required
    "Content-Type": "application/json"
}

def list_tools():
    # Smithery expects a GET to /mcp for tool discovery
    response = requests.get(MCP_SERVER_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    print("Available tools:", response.json())

def call_tool(tool_name, params):
    # For custom MCPs, you usually POST to /mcp with tool name and params
    payload = {
        "tool": tool_name,
        "params": params
    }
    response = requests.post(MCP_SERVER_URL, json=payload, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

    # List available tools
    list_tools()

    # Example: call a tool (replace with your actual tool and params)
    # result = call_tool("summarize", {"text": "Your research paper text here"})
    # print("Tool result:", result) 