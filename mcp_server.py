import asyncio
import logging
import os
from typing import Any
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Configure minimal logging
logging.basicConfig(level=logging.WARNING)  # Reduced logging level
logger = logging.getLogger("pdf-summarizer-mcp")

# Create server instance
server = Server("pdf-summarizer-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools - must be ultra-fast."""
    # Return tools immediately without any imports or initialization
    return [
        types.Tool(
            name="summarize_pdf_from_url",
            description="Download and summarize a PDF from a URL using Google Gemini AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the PDF to download and summarize"
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="summarize_pdf_text",
            description="Summarize provided PDF text using Google Gemini AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text content of the PDF to summarize"
                    }
                },
                "required": ["text"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Handle tool calls - all heavy imports happen here."""
    try:
        # Import heavy modules only when tool is actually called
        from app.summarizer import get_summary
        from app.utils import extract_text_from_pdf, download_pdf_content
        
        if name == "summarize_pdf_from_url":
            url = arguments.get("url")
            if not url:
                return [types.TextContent(type="text", text="Error: URL is required")]
            
            # Download and process PDF
            pdf_content_bytes = download_pdf_content(url)
            pdf_text = extract_text_from_pdf(pdf_content_bytes)
            
            if not pdf_text.strip():
                return [types.TextContent(
                    type="text", 
                    text="Error: Could not extract text from PDF. It might be image-only or corrupted."
                )]
            
            # Generate summary
            summary = get_summary(pdf_text)
            
            return [types.TextContent(
                type="text",
                text=f"PDF Summary from {url}:\n\n{summary}"
            )]
            
        elif name == "summarize_pdf_text":
            text = arguments.get("text")
            if not text:
                return [types.TextContent(type="text", text="Error: Text is required")]
            
            # Generate summary
            summary = get_summary(text)
            
            return [types.TextContent(
                type="text",
                text=f"PDF Text Summary:\n\n{summary}"
            )]
        
        else:
            return [types.TextContent(type="text", text=f"Error: Unknown tool {name}")]
            
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Main entry point - minimal initialization."""
    # Check if API key exists but don't initialize anything
    if not os.getenv("GEMINI_API_KEY"):
        logger.warning("GEMINI_API_KEY not set - tools will fail when called")
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pdf-summarizer-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())