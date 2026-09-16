#!/usr/bin/env python3
"""MCP client test voor showet_mcp_server (mcp 2.x API)."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    cwd = "/home/hans/.openclaw/workspace/projects/showet"
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["showet_mcp_server.py"],
        cwd=cwd,
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("=== Tools ===")
            tools = await session.list_tools()
            for name, desc in tools:
                print(f"  - {name}: {desc}")
            
            print("\n=== Test: showet_list_platforms ===")
            result = await session.call_tool("showet_list_platforms", {})
            print(f"  Result type: {type(result)}")
            content = result.content if hasattr(result, 'content') else result
            print(f"  Content: {content[:200] if hasattr(content, '__getitem__') else content}")
            
            print("\n=== Test: showet_search_demos (batman) ===")
            result = await session.call_tool("showet_search_demos", {"query": "batman"})
            content = result.content if hasattr(result, 'content') else result
            print(f"  Content: {str(content)[:300]}")

if __name__ == "__main__":
    asyncio.run(main())
