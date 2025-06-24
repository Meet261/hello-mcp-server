# Paper Summarizer (MCP)

This project is a web application built with FastAPI (Python) and a simple HTML/CSS/JavaScript frontend. It allows users to upload a PDF file or provide a PDF link to get a concise summary of the academic paper, powered by Google's Gemini large language model.

The application is designed for deployment on Smithery.ai as a Micro-service Compatible Platform (MCP) server.

## 📁 Project Structure

```
mcp-paper-summarizer/
├── app/
│   ├── main.py             # FastAPI server exposing API endpoints and serving UI
│   ├── summarizer.py       # LLM logic for summarizing PDFs using Gemini API
│   └── utils.py            # PDF downloading, text extraction utilities
├── static/
│   └── style.css           # Custom CSS styling for the UI
│   └── script.js           # Frontend logic for interactive elements
├── templates/
│   └── index.html          # Frontend UI for PDF upload/URL input
├── requirements.txt        # Python dependencies for the backend
├── Dockerfile              # Docker configuration for containerization
├── smithery.yaml           # Smithery.ai specific deployment configuration
└── README.md               # Project documentation
```

## ✨ Features

- **PDF Upload**: Summarize papers by uploading a PDF file directly from your computer.
- **PDF URL Input**: Summarize papers by providing a direct link to a PDF file (e.g., from arXiv).
- **AI-Powered Summarization**: Uses Google's powerful Gemini 2.0 Flash API to generate concise and relevant summaries.
- **User-Friendly Interface**: A clean, responsive, and easy-to-use web interface built with HTML, modern CSS (Tailwind CSS), and JavaScript (script.js) for dynamic interactions.

## 🛠 Setup and Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/Meet261/hello-mcp-server.git
cd hello-mcp-server
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Your Google Gemini API Key

- Visit [Google AI Studio](https://makersuite.google.com/)
- Log in with your Google account.
- Click “Create API key in new project” and copy the key.

### 5. Configure Your API Key Locally

Create a `.env` file in your root project directory:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

Also add `.env` to `.gitignore` to keep your key secret:

```
.env
```

### 6. Run the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Access in your browser:

```
http://127.0.0.1:8000/
```

## 🚀 Deployment to Smithery.ai

### 1. Push Your Code to GitHub

```bash
git add .
git commit -m "Initial commit of paper summarizer MCP"
git push origin main
```

### 2. Log in to Smithery.ai

- Go to [smithery.ai](https://smithery.ai)
- Create a new project and connect your GitHub repository.

### 3. Configure Environment Variables

In your project settings:

- **Key**: `GEMINI_API_KEY`
- **Value**: Paste your Gemini API key (no quotes)

### 4. Initiate Deployment

Smithery uses your `Dockerfile` and `smithery.yaml` to build the image.

### 5. Access Your Live App

After a successful deployment, Smithery provides a public URL — use it to access your deployed summarizer!

---

Enjoy your AI-powered research assistant! 🧠📄
