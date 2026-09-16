#!/usr/bin/env python3
"""Showet MCP Server — exposes the Showet demo-runner as MCP tools.

This lets any MCP-capable agent (GLaDOS, Wheatley, jaison-core, airi,
mcp-this, an LLM IDE, etc.) drive Showet: list platforms, search Pouet.net
demos (with optional platform filter), fetch demo metadata, get offline
recommendations, and prepare a demo for playback.

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

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Make showet's own modules importable from this script's directory.
PROJECT_ROOT = Path(__file__).parent
import sys  # noqa: E402

sys.path.insert(0, str(PROJECT_ROOT))

from showet_api import get_api  # the singleton high-level API  # noqa: E402
from party_calendar import get_upcoming_parties, get_party_winners  # noqa: E402

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
                        "query (e.g. '64k intro 2024', 'amiga'). Supports "
                        "optional platform filter. Returns id, name, type, "
                        "score, platform.",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term."},
                    "limit": {"type": "integer", "default": 20,
                              "description": "Max results."},
                    "platform": {"type": "string", "default": "",
                                 "description": "Optional platform slug filter "
                                                "(e.g. 'commodore_64')."},
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
            name="showet_get_recommendations",
            description="Get offline demo recommendations based on local "
                        "favorites and viewing history. Returns a ranked list "
                        "of Pouet.net production IDs. Works without an API key.",
            input_schema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10,
                              "description": "Max recommendations."},
                },
                "required": [],
            },
        ),
        types.Tool(
            name="showet_get_status",
            description="Showet runtime status: number of platforms loaded, "
                        "the platform list, version, and whether the "
                        "nostalgist.js manifest is present.",
            input_schema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="showet_get_playlists",
            description="Get all demo playlists (named collections of Pouet.net IDs).",
            input_schema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="showet_list_favorites",
            description="List all favorite demos with metadata (id, name, platform, notes, added_at).",
            input_schema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="showet_add_favorite",
            description="Add a demo to favorites (id, name, platform, notes).",
            input_schema={
                "type": "object",
                "properties": {
                    "pouet_id": {"type": "integer", "description": "Pouet.net production ID."},
                    "name": {"type": "string", "description": "Demo name."},
                    "platform": {"type": "string", "default": "", "description": "Platform slug."},
                    "notes": {"type": "string", "default": "", "description": "User notes."},
                },
                "required": ["pouet_id", "name"],
            },
        ),
        types.Tool(
            name="showet_remove_favorite",
            description="Remove a demo from favorites by Pouet.net ID.",
            input_schema={
                "type": "object",
                "properties": {
                    "pouet_id": {"type": "integer", "description": "Pouet.net production ID."},
                },
                "required": ["pouet_id"],
            },
        ),
        types.Tool(
            name="showet_get_history",
            description="Get recent viewing history (demo ID, platform, played_at, score).",
            input_schema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 50, "description": "Max entries."},
                },
                "required": [],
            },
        ),
        types.Tool(
            name="showet_get_upcoming_parties",
            description="Get upcoming demoscene parties from Pouet.net calendar "
                        "(or fallback list). Returns name, date, location, type, link.",
            input_schema={
                "type": "object",
                "properties": {
                    "days_ahead": {
                        "type": "integer",
                        "default": 90,
                        "description": "How many days ahead to look.",
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="showet_get_party_winners",
            description="Get known winning demos from a specific demoparty "
                        "(e.g. 'revision', 'breakpoint').",
            input_schema={
                "type": "object",
                "properties": {
                    "party_name": {
                        "type": "string",
                        "description": "Party name (case-insensitive, e.g. 'revision').",
                    },
                    "year": {
                        "type": "integer",
                        "description": "Optional year filter.",
                    },
                },
                "required": ["party_name"],
            },
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
            platform_filter = args.get("platform") or None
            result = _api().search_demos(
                args.get("query", ""), int(args.get("limit", 20)),
                platform=platform_filter,
            )
        elif name == "showet_get_demo_info":
            result = _api().get_demo_info(int(args["pouet_id"]))
        elif name == "showet_run_demo":
            plat = args.get("platform") or None
            result = _api().run_demo(int(args["pouet_id"]), plat)
        elif name == "showet_get_recommendations":
            result = _api().get_recommendations(int(args.get("limit", 10)))
        elif name == "showet_get_status":
            result = _api().get_status()
        elif name == "showet_get_status_extended":
            result = _api().get_status_extended()
        elif name == "showet_get_playlists":
            result = _api().get_playlists()
        elif name == "showet_list_favorites":
            result = _api().list_favorites()
        elif name == "showet_add_favorite":
            result = _api().add_favorite(
                int(args["pouet_id"]),
                args.get("name", ""),
                args.get("platform", ""),
                args.get("notes", ""),
            )
        elif name == "showet_remove_favorite":
            result = _api().remove_favorite(int(args["pouet_id"]))
        elif name == "showet_get_history":
            result = _api().get_history(int(args.get("limit", 50)))
        elif name == "showet_get_upcoming_parties":
            result = get_upcoming_parties(int(args.get("days_ahead", 90)))
        elif name == "showet_get_party_winners":
            party_name = args["party_name"]
            year_raw = args.get("year")
            year = int(year_raw) if year_raw is not None else None
            result = get_party_winners(party_name, year)
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
