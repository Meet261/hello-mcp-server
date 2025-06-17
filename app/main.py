from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/mcp")
async def handle_mcp(request: Request):
    params = dict(request.query_params)
    api_key = params.get("apiKey", "not provided")
    return JSONResponse(content={
        "message": "Hello, MCP World!",
        "receivedApiKey": api_key
    })
