# MCP Summarization Server

A deployable MCP server for Smithery that summarizes research papers using the Gemini API. Users can upload a PDF or provide a URL to a paper, and receive a summary.

## Features
- Upload PDF or enter URL of a research paper
- Summarizes using Google Gemini API
- Deployable to [smithery.ai](https://smithery.ai)

## Project Structure
```
backend/   # FastAPI MCP server
frontend/  # React UI (Vite)
smithery.yaml
```

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deployment to Smithery
1. Push your code (including `smithery.yaml` and Dockerfiles) to GitHub.
2. Connect your GitHub to Smithery.
3. Deploy via the Smithery dashboard.

## Configuration
- Requires a Gemini API key (see [Google Gemini](https://ai.google.com/gemini)).
- Smithery will pass this as a config parameter.

## License
MIT 