from fastapi import FastAPI

app = FastAPI()

@app.get("/mcp")
async def handle_mcp():
    return {"message": "Hello, MCP World!"}
