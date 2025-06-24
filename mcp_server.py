#!/usr/bin/env python3
import asyncio
import json
import sys
from typing import Any, Dict, List

async def handle_initialize(params: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "pdf-summarizer-mcp",
            "version": "0.1.0"
        }
    }

async def handle_list_tools(params: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "summarize_pdf_from_url",
                "description": "Download and summarize a PDF from a URL using Google Gemini AI",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL of the PDF to download and summarize"
                        }
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "summarize_pdf_text", 
                "description": "Summarize provided PDF text using Google Gemini AI",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text content of the PDF to summarize"
                        }
                    },
                    "required": ["text"]
                }
            }
        ]
    }

async def handle_call_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Import heavy modules only when actually called
        from app.summarizer import get_summary
        from app.utils import extract_text_from_pdf, download_pdf_content
        
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if name == "summarize_pdf_from_url":
            url = arguments.get("url")
            if not url:
                return {
                    "content": [{"type": "text", "text": "Error: URL is required"}]
                }
            
            pdf_content_bytes = download_pdf_content(url)
            pdf_text = extract_text_from_pdf(pdf_content_bytes)
            
            if not pdf_text.strip():
                return {
                    "content": [{"type": "text", "text": "Error: Could not extract text from PDF"}]
                }
            
            summary = get_summary(pdf_text)
            return {
                "content": [{"type": "text", "text": f"PDF Summary:\n\n{summary}"}]
            }
            
        elif name == "summarize_pdf_text":
            text = arguments.get("text")
            if not text:
                return {
                    "content": [{"type": "text", "text": "Error: Text is required"}]
                }
            
            summary = get_summary(text)
            return {
                "content": [{"type": "text", "text": f"Summary:\n\n{summary}"}]
            }
        
        return {
            "content": [{"type": "text", "text": f"Unknown tool: {name}"}]
        }
        
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error: {str(e)}"}]
        }

async def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "initialize":
        return await handle_initialize(params)
    elif method == "tools/list":
        return await handle_list_tools(params)
    elif method == "tools/call":
        return await handle_call_tool(params)
    else:
        raise Exception(f"Unknown method: {method}")

async def main():
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            
            try:
                result = await handle_request(request)
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0", 
                    "id": request.get("id"),
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
            
            print(json.dumps(response), flush=True)
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())