#!/usr/bin/env python3
import json
import sys
import logging

logging.disable(logging.CRITICAL)

def send_response(response):
    print(json.dumps(response), flush=True)

def get_all_tools():
    """Define all available tools"""
    return [
        # PDF Tools
        {
            "name": "summarize_pdf_from_url",
            "description": "Download and summarize a PDF from URL",
            "inputSchema": {
                "type": "object",
                "properties": {"url": {"type": "string", "description": "PDF URL"}},
                "required": ["url"]
            }
        },
        {
            "name": "summarize_text",
            "description": "Summarize provided text using AI",
            "inputSchema": {
                "type": "object",
                "properties": {"text": {"type": "string", "description": "Text to summarize"}},
                "required": ["text"]
            }
        },
        
        # Web Tools
        {
            "name": "search_web",
            "description": "Search the web for information",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "number", "description": "Number of results (default: 5)"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "scrape_webpage",
            "description": "Extract text content from a webpage",
            "inputSchema": {
                "type": "object",
                "properties": {"url": {"type": "string", "description": "Webpage URL"}},
                "required": ["url"]
            }
        },
        {
            "name": "get_weather",
            "description": "Get weather information for a location",
            "inputSchema": {
                "type": "object",
                "properties": {"location": {"type": "string", "description": "City or location name"}},
                "required": ["location"]
            }
        },
        
        # AI Tools
        {
            "name": "chat_with_openai",
            "description": "Chat with OpenAI models",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Message to send"},
                    "model": {"type": "string", "description": "Model to use (default: gpt-3.5-turbo)"}
                },
                "required": ["message"]
            }
        },
        {
            "name": "translate_text",
            "description": "Translate text to another language",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to translate"},
                    "target_language": {"type": "string", "description": "Target language (default: Spanish)"}
                },
                "required": ["text"]
            }
        },
        {
            "name": "analyze_sentiment",
            "description": "Analyze sentiment of text",
            "inputSchema": {
                "type": "object",
                "properties": {"text": {"type": "string", "description": "Text to analyze"}},
                "required": ["text"]
            }
        },
        
        # Data Tools
        {
            "name": "parse_json",
            "description": "Parse and format JSON data",
            "inputSchema": {
                "type": "object",
                "properties": {"json_string": {"type": "string", "description": "JSON string to parse"}},
                "required": ["json_string"]
            }
        },
        {
            "name": "parse_csv",
            "description": "Parse CSV data and return formatted table",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "csv_string": {"type": "string", "description": "CSV data to parse"},
                    "delimiter": {"type": "string", "description": "CSV delimiter (default: comma)"}
                },
                "required": ["csv_string"]
            }
        },
        {
            "name": "extract_emails",
            "description": "Extract email addresses from text",
            "inputSchema": {
                "type": "object",
                "properties": {"text": {"type": "string", "description": "Text to search for emails"}},
                "required": ["text"]
            }
        },
        {
            "name": "extract_urls",
            "description": "Extract URLs from text",
            "inputSchema": {
                "type": "object",
                "properties": {"text": {"type": "string", "description": "Text to search for URLs"}},
                "required": ["text"]
            }
        }
    ]

def handle_tool_call(name: str, arguments: dict) -> str:
    """Route tool calls to appropriate handlers"""
    try:
        # PDF Tools
        if name in ["summarize_pdf_from_url", "summarize_text"]:
            from tools.pdf_tools import summarize_pdf_from_url, summarize_text
            
            if name == "summarize_pdf_from_url":
                url = arguments.get("url")
                if not url:
                    return "Error: URL is required"
                return summarize_pdf_from_url(url)
            
            elif name == "summarize_text":
                text = arguments.get("text")
                if not text:
                    return "Error: Text is required"
                return summarize_text(text)
        
        # Web Tools
        elif name in ["search_web", "scrape_webpage", "get_weather"]:
            from tools.web_tools import search_web, scrape_webpage, get_weather
            
            if name == "search_web":
                query = arguments.get("query")
                num_results = arguments.get("num_results", 5)
                if not query:
                    return "Error: Search query is required"
                return search_web(query, num_results)
            
            elif name == "scrape_webpage":
                url = arguments.get("url")
                if not url:
                    return "Error: URL is required"
                return scrape_webpage(url)
            
            elif name == "get_weather":
                location = arguments.get("location")
                if not location:
                    return "Error: Location is required"
                return get_weather(location)
        
        # AI Tools
        elif name in ["chat_with_openai", "translate_text", "analyze_sentiment"]:
            from tools.ai_tools import chat_with_openai, translate_text, analyze_sentiment
            
            if name == "chat_with_openai":
                message = arguments.get("message")
                model = arguments.get("model", "gpt-3.5-turbo")
                if not message:
                    return "Error: Message is required"
                return chat_with_openai(message, model)
            
            elif name == "translate_text":
                text = arguments.get("text")
                target_language = arguments.get("target_language", "Spanish")
                if not text:
                    return "Error: Text is required"
                return translate_text(text, target_language)
            
            elif name == "analyze_sentiment":
                text = arguments.get("text")
                if not text:
                    return "Error: Text is required"
                return analyze_sentiment(text)
        
        # Data Tools
        elif name in ["parse_json", "parse_csv", "extract_emails", "extract_urls"]:
            from tools.data_tools import parse_json, parse_csv, extract_emails, extract_urls
            
            if name == "parse_json":
                json_string = arguments.get("json_string")
                if not json_string:
                    return "Error: JSON string is required"
                return parse_json(json_string)
            
            elif name == "parse_csv":
                csv_string = arguments.get("csv_string")
                delimiter = arguments.get("delimiter", ",")
                if not csv_string:
                    return "Error: CSV string is required"
                return parse_csv(csv_string, delimiter)
            
            elif name == "extract_emails":
                text = arguments.get("text")
                if not text:
                    return "Error: Text is required"
                return extract_emails(text)
            
            elif name == "extract_urls":
                text = arguments.get("text")
                if not text:
                    return "Error: Text is required"
                return extract_urls(text)
        
        else:
            return f"Unknown tool: {name}"
            
    except ImportError as e:
        return f"Tool not available: {str(e)}"
    except Exception as e:
        return f"Tool execution failed: {str(e)}"

def handle_request(request):
    """Handle incoming JSON-RPC request"""
    method = request.get("method", "")
    request_id = request.get("id")
    params = request.get("params", {})
    
    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "multi-tool-mcp-server",
                        "version": "0.1.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": get_all_tools()
                }
            }
        
        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            result = handle_tool_call(name, arguments)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": result}]
                }
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
            
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }

def main():
    """Main server loop"""
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                request = json.loads(line)
                response = handle_request(request)
                send_response(response)
                
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                send_response(error_response)
                
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()