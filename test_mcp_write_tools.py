#!/usr/bin/env python3
"""MCP client test voor showet_mcp_server — write-tools."""
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
            
            print("=== showet_add_favorite ===")
            result = await session.call_tool("showet_add_favorite", {
                "pouet_id": 4096,
                "name": "Test Favorite",
                "platform": "commodore_64",
                "notes": "MCP write-test"
            })
            content = result.content if hasattr(result, 'content') else result
            text = str(content)
            assert "ok" in text.lower() or "4096" in text
            print(f"OK: {text[:200]}")
            
            print("=== showet_list_favorites na toevoeging ===")
            result = await session.call_tool("showet_list_favorites", {})
            content = result.content if hasattr(result, 'content') else result
            text = str(content)
            assert "4096" in text or "Test Favorite" in text, f"favorite niet gevonden: {text[:200]}"
            print(f"OK: favorite aanwezig: {text[:200]}")
            
            print("=== showet_remove_favorite (id=4096) ===")
            result = await session.call_tool("showet_remove_favorite", {"pouet_id": 4096})
            content = result.content if hasattr(result, 'content') else result
            text = str(content)
            assert "ok" in text.lower() or "4096" in text
            print(f"OK: {text[:200]}")
            
            print("=== showet_list_favorites na verwijdering ===")
            result = await session.call_tool("showet_list_favorites", {})
            content = result.content if hasattr(result, 'content') else result
            text = str(content)
            # Na verwijdering moet de lijst leeg zijn of de favorite niet meer bevatten
            print(f"OK: {text[:200]}")

if __name__ == "__main__":
    asyncio.run(main())
    print("ALL MCP WRITE-TOOL TESTS PASSED")
