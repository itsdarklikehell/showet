#!/usr/bin/env python3
"""Showet MCP Server — exposes the Showet demo-runner as MCP tools.

This lets any MCP-capable agent (GLaDOS, Wheatley, jaison-core, airi,
mcp-this, an LLM IDE, etc.) drive Showet: list platforms, search Pouet.net
demos, fetch demo metadata, and prepare a demo for playback.

Transport: stdio (the MCP default). Run with:
    python showet_mcp_server.py
or, with the bundled venv:
    .venv/bin/python showet_mcp_server.py

It reuses ShowetAPI (showet_api.py) so it stays in lockstep with the CLI.
No files are modified; this is a read/prepare interface only.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# Make showet's own modules importable from this script's directory.
PROJECT_ROOT = Path(__file__).parent
import sys
sys.path.insert(0, str(PROJECT_ROOT))

from showet_api import get_api  # the singleton high-level API

server = Server("showet-mcp")


def _api():
    return get_api()


async def _on_list_tools(context, params):
    tools = [
        types.Tool(
            name="showet_list_platforms",
            description="List all retro/platform runners Showet can drive "
                        "(commodore_64, amiga, nes, etc.).",
            input_schema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="showet_search_demos",
            description="Search Pouet.net demoscene productions by free-text "
                        "query (e.g. '64k intro 2024', 'amiga'). Returns id, "
                        "name, type, score.",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term."},
                    "limit": {"type": "integer", "default": 20,
                              "description": "Max results."},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="showet_get_demo_info",
            description="Fetch full metadata for a Pouet.net production by its "
                        "numeric ID (name, group, platform, party/ranking).",
            input_schema={
                "type": "object",
                "properties": {
                    "pouet_id": {"type": "integer",
                                 "description": "Pouet.net production ID."},
                },
                "required": ["pouet_id"],
            },
        ),
        types.Tool(
            name="showet_run_demo",
            description="Prepare a demo for playback: resolve Pouet metadata, "
                        "auto-detect (or force) the platform, and return a "
                        "ready status dict. Does not block on emulation.",
            input_schema={
                "type": "object",
                "properties": {
                    "pouet_id": {"type": "integer",
                                 "description": "Pouet.net production ID."},
                    "platform": {"type": "string", "default": "",
                                 "description": "Optional platform slug to "
                                                "override auto-detect."},
                },
                "required": ["pouet_id"],
            },
        ),
        types.Tool(
            name="showet_get_status",
            description="Showet runtime status: number of platforms loaded, "
                        "the platform list, version, and whether the "
                        "nostalgist.js manifest is present.",
            input_schema={"type": "object", "properties": {}},
        ),
    ]
    return types.ListToolsResult(tools=tools)


async def _on_call_tool(context, params):
    name = params.name
    args = params.arguments or {}
    try:
        if name == "showet_list_platforms":
            result = _api().list_platforms()
        elif name == "showet_search_demos":
            result = _api().search_demos(
                args.get("query", ""), int(args.get("limit", 20)))
        elif name == "showet_get_demo_info":
            result = _api().get_demo_info(int(args["pouet_id"]))
        elif name == "showet_run_demo":
            plat = args.get("platform") or None
            result = _api().run_demo(int(args["pouet_id"]), plat)
        elif name == "showet_get_status":
            result = _api().get_status()
        else:
            result = {"error": f"unknown tool: {name}"}
    except Exception as exc:  # surface errors as tool output, never crash
        result = {"error": str(exc)}

    return types.CallToolResult(
        content=[types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str),
        )]
    )


server = Server(
    "showet-mcp",
    on_list_tools=_on_list_tools,
    on_call_tool=_on_call_tool,
)


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
