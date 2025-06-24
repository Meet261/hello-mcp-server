import asyncio
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions

server = Server("test-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="hello",
            description="Say hello",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    return [types.TextContent(type="text", text="Hello from MCP server!")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(
            server_name="test-server", server_version="0.1.0",
            capabilities=server.get_capabilities()
        ))

if __name__ == "__main__":
    asyncio.run(main())