# 🚀 Hello MCP Server

A simple FastAPI-based web service that returns a greeting message.  
Built for deployment on [Smithery](https://smithery.ai) using containerization.

## 🌐 Live Demo

> Once deployed, your service will be available at:  
> `https://your-smithery-project.smithery.run/`

## 🧩 Features

- Lightweight FastAPI web server
- Dockerized for easy deployment
- Compatible with MCP environments (e.g., Smithery)
- Returns: `{"message": "Hello, MCP World!"}` at `/`

---

## 📁 Project Structure

```
hello-mcp-server/
├── app/
│   └── main.py          # FastAPI application
├── Dockerfile           # Docker build instructions
├── requirements.txt     # Python dependencies
└── smithery.yaml        # Smithery deployment configuration
```

---

## 🛠️ Local Development

### 1. Install requirements (optional)
```bash
pip install -r requirements.txt
```

### 2. Run the server locally
```bash
uvicorn app.main:app --reload --port 8080
```

Open browser: [http://localhost:8080](http://localhost:8080)

---

## 🐳 Docker Usage

### Build the Docker image

```bash
docker build -t hello-mcp-server .
```

### Run the container

```bash
docker run -p 8080:8080 hello-mcp-server
```

---

## 🚀 Deploy to Smithery

1. Push this project to a GitHub repository.
2. Go to [smithery.ai](https://smithery.ai) → **New Project**
3. Paste your repo URL.
4. Smithery will auto-deploy using `smithery.yaml`.

---

## 📄 Endpoint

| Method | Path | Description                 |
|--------|------|-----------------------------|
| GET    | `/`  | Returns Hello MCP message   |

Response:

```json
{
  "message": "Hello, MCP World!"
}
```

---

## 📦 Dependencies

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
