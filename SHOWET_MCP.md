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
| `showet_search_demos` | Search Pouet.net by query; returns id/name/type/score. |
| `showet_get_demo_info` | Full metadata for a Pouet production by numeric ID. |
| `showet_run_demo` | Prepare a demo for playback (resolve metadata, detect/force platform). |
| `showet_get_status` | Runtime status: platforms loaded, version, nostalgist manifest. |

## Run
```bash
cd /home/rizzo/.openclaw/workspace/projects/showet
.venv/bin/python showet_mcp_server.py          # stdio transport
```
A venv with `mcp` is bundled at `.venv/` (created during the build). To recreate:
`python3 -m venv .venv && .venv/bin/pip install mcp`.

## Register with an MCP client
Add to your client's server config (e.g. `.mcp.json` or Claude Desktop /
jaison-core / airi settings):
```json
{
  "mcpServers": {
    "showet": {
      "command": "/home/rizzo/.openclaw/workspace/projects/showet/.venv/bin/python",
      "args": ["/home/rizzo/.openclaw/workspace/projects/showet/showet_mcp_server.py"]
    }
  }
}
```
The server is read/prepare-only — it never modifies files or launches
emulation unsupervised; `showet_run_demo` returns a prepared status dict.

## Notes
- Wraps `showet_api.ShowetAPI` (singleton), so it stays in lockstep with the CLI.
- Written against `mcp` 2.0.0 using the stable low-level `Server` API
  (constructor `on_list_tools` / `on_call_tool` handlers, `input_schema`).
- Tested: `initialize` + `tools/list` + `showet_get_status` / `showet_list_platforms`
  return live data (91 platforms). `search`/`info`/`run` require network (Pouet API).
