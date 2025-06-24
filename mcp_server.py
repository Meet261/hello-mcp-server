#!/usr/bin/env python3
import json
import sys
import os

def main():
    # Read from stdin line by line
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            method = request.get("method")
            request_id = request.get("id")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "test-server", "version": "0.1.0"}
                    }
                }
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "tools": [{
                            "name": "hello",
                            "description": "Say hello",
                            "inputSchema": {"type": "object", "properties": {}}
                        }]
                    }
                }
            elif method == "tools/call":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id, 
                    "result": {
                        "content": [{"type": "text", "text": "Hello from MCP server!"}]
                    }
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
                
            print(json.dumps(response), flush=True)
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()