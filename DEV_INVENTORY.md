# Showet Development Inventory — 2026-09-15

## Status
- Repo: `hmol33/showet` (origineel), gekloond op `master`
- Upstream: `origin/master` = `4368711` (local == remote, geen commits achter/bij)
- Push-rechten: `hmol33` → `hmol33/showet` (push OK, token valid)
- Branch: `master`

## Wat er werkt (lokaal getest)
- `showet --platforms` → 91 platformen
- `showet --help` → CLI werkt
- `showet-api --help` → API server conceptueel OK
- `showet-status` → dashboard + FFmpeg + RetroArch beschikbaar
- MCP-server via `showet_mcp_server.py` → live getest met `test_mcp_client.py`:
  - Server start, tools list werkt, 14 tools beschikbaar
  - `showet_list_platforms` → 91 platformen terug
  - `showet_search_demos("batman")` → Batman demos gevonden (Pouet.net)
  - Alle tools: list, search, get_demo_info, run_demo, get_recommendations, get_status, playlists, favorites CRUD, history
- Dependencies: pip install -e ".[web]" → OK (fastapi, uvicorn, mcp, inquirer, patool, requests, aiohttp, feedparser, websockets)

## Wat er niet werkt (bekend / geen blocker)
- `mcp` import faalt zonder juiste venv + pydantic_core fix → opgelost door pydantic-core==2.46.4 te force-reinstall
- `test_mcp_client.py` (de test die ik geschreven heb) — uncommit, is een validation-tool
- Geen emulators geinstalleerd (RetroArch aanwezig maar geen specifieke cores voor test-demos)
- Geen echte demo testbaar zonder Pouet.net API key + demo-bestanden (offline)

## Skills-potential
- Showet MCP-server is live en werkend — dit kan een **Hermes skill** worden voor GLaDOS om demos te spelen/vinden aan te raden via MCP
- Ideaal voor een `showet-mcp` skill: documenteer de tools, geef gebruiksaanwijzing, koppel aan GLaDOS
- Home Assistant integratie: `showet_webui.py` + `showet_webui_nostalgist.py` → relevant voor de Kapitein's HA setup
- Demo-viewer + CRT-shader + streaming → relevant voor showcase

## Volgende stap (als Kapitein dit goedkeurt)
1. Commit `test_mcp_client.py` als validatie-tool voor de MCP-server
2. Push naar hmol33/showet
3. Maak een `showet-mcp` skill in `~/.hermes/skills/` die GLaDOS instrueert hoe de Showet MCP-server te gebruiken
4. Of kies next project (Open-LLM-VTuber) als showet "genoeg" is

## Notities
- Upstream (hmol33/master) is up-to-date — geen sync-issue
- Geen issues/PRs open op hmol33/showet (check via `gh issue list` → geen issues)
- README.md is uitgebreid (537 regels), documenteert CLI, streaming, CRT, platformen, nostalgist
- MCP-server is de meest interessante component voor AI-agent integratie
