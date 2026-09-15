#!/usr/bin/env python3
"""MCP client test voor showet_mcp_server via hermes-venv python."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    cwd = "/home/hans/.openclaw/workspace/projects/showet"
    server_params = StdioServerParameters(
        command="/home/hans/.hermes/hermes-agent/venv/bin/python",
        args=["showet_mcp_server.py"],
        cwd=cwd,
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=== showet_list_platforms ===")
            result = await session.call_tool("showet_list_platforms", {})
            content = result.content if hasattr(result, 'content') else result
            text = str(content)
            assert "alambik_alambik" in text, f"platformen niet gevonden in: {text[:200]}"
            print(f"OK: {text.count(chr(10))} regels platformen")
            
            print("=== showet_get_status ===")
            result = await session.call_tool("showet_get_status", {})
            content = result.content if hasattr(result, 'content') else result
            text = str(content)
            assert "platforms_loaded" in text
            print(f"OK: {text[:150]}")
            
            print("=== showet_get_demo_info (id=12345) ===")
            result = await session.call_tool("showet_get_demo_info", {"pouet_id": 12345})
            content = result.content if hasattr(result, 'content') else result
            text = str(content)
            assert "12345" in text
            print(f"OK: {text[:150]}")
            
            print("=== showet_run_demo (id=12345) ===")
            result = await session.call_tool("showet_run_demo", {"pouet_id": 12345})
            content = result.content if hasattr(result, 'content') else result
            text = str(content)
            assert "ready" in text or "prepared" in text
            print(f"OK: {text[:150]}")

if __name__ == "__main__":
    asyncio.run(main())
    print("ALL MCP VERIFICATION TESTS PASSED")
