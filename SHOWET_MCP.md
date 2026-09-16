# Showet MCP Server

Exposes the Showet demoscene runner as **Model Context Protocol** tools, so
any MCP-capable agent (GLaDOS, Wheatley, jaison-core, airi, mcp-this, an LLM
IDE, etc.) can drive Showet programmatically.

Built by GLaDOS (Hermes) as part of the joint GLaDOS ↔ Wheatley showet
deep-dive. Wheatley (OpenClaw) concurrently ported ReShade CRT shaders into
the WebGL shader playground (`showet_crt_reshade.js`).

## Tools

| Tool | Purpose |
|------|---------|
| `showet_list_platforms` | List all platform runners (91+, e.g. `commodore_64`, `amiga`, `nes`). |
| `showet_search_demos` | Search Pouet.net by query (+ optional platform filter); returns id/name/type/score/platform. |
| `showet_get_demo_info` | Full metadata for a Pouet production by numeric ID. |
| `showet_run_demo` | Prepare a demo for playback (resolve metadata, detect/force platform). |
| `showet_get_recommendations` | Offline demo recommendations from local favorites/history. |
| `showet_get_status` | Runtime status: platforms loaded, version, nostalgist manifest. |
| `showet_get_status_extended` | Extended status: + demo_db ready, db_path, platform_count, streaming backend. |
| `showet_list_favorites` | List all favorite demos with metadata (id, name, platform, notes, added_at). |
| `showet_add_favorite` | Add a demo to favorites (id, name, platform, notes). |
| `showet_remove_favorite` | Remove a demo from favorites by Pouet.net ID. |
| `showet_get_history` | Get recent viewing history (demo ID, platform, played_at, score). |
| `showet_get_playlists` | Get all demo playlists (named collections of Pouet.net IDs). |

**Totaal: 12 tools.**

## Run

```bash
cd /home/hans/.openclaw/workspace/projects/showet
.venv/bin/python showet_mcp_server.py          # stdio transport
```

Een venv met `mcp` is gebundled bij `.venv/` (aangemaakt tijdens de build).
Teruggestarten: `python3 -m venv .venv && .venv/bin/pip install mcp`.

## Register with an MCP client

Voeg toe aan de MCP-client config (bijv. `.mcp.json` of Claude Desktop /
jaison-core / airi settings):

```json
{
  "mcpServers": {
    "showet": {
      "command": "/home/hans/.openclaw/workspace/projects/showet/.venv/bin/python",
      "args": ["/home/hans/.openclaw/workspace/projects/showet/showet_mcp_server.py"]
    }
  }
}
```

De server is read/prepare-only — het modifyt geen bestanden en start geen
emulatie unsupervised; `showet_run_demo` returned alleen een prepared status dict.

## Notes

- Wraps `showet_api.ShowetAPI` (singleton), dus blijft het in lockstep met de CLI.
- Geschreven tegen `mcp` 2.x met de stabiele low-level `Server` API
  (constructor `on_list_tools` / `on_call_tool` handlers, `input_schema`).
-`get_recommendations`, `list_favorites`, `add_favorite`, `remove_favorite`,
  `get_history`, `get_playlists` werken offline zonder Pouet.net API.
- `search_demos`, `get_demo_info`, `run_demo` vereisen netwerk (Pouet API).

## Skills

Deze MCP-server is onderdeel van de showet project-familie. Voor verdere
ontwikkeling zie:
- Kanban-taak: "showet: MCP-server uitbreiding met nieuwe tools"
- Repository: `https://github.com/itsdarklikehell/showet`
