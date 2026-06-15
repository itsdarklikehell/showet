# showet

**Demo viewer using Pouet.net's metadata** - Consider this "MAME for demos"

**🕹️ 78 platforms supported** including C64, Amiga, Atari, Nintendo, Sega, Sony PlayStation, and more.

![](showet-ui/screenshot-web.png?raw=true "Web UI Screenshot")

Developed on Ubuntu, other platforms may work.

## Quick Start

```bash
# Install (editable mode for development)
python3 -m pip install -e .

# CLI mode
showet --platforms     # List supported platforms
showet 12345         # Run demo by pouet.net ID

# Web UI mode
showet-webui         # Starts API + opens browser
```

## Installation

```bash
git clone https://github.com/itsdarklikehell/showet
cd showet
./install.sh --install-showet
./install.sh --install-emulators
```

For development or testing without system installation:
```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
```

## Architecture

- **showet.py** - Core CLI logic, pouet.net API integration
- **platformcommon.py** - Base class with file discovery & process execution
- **Platform_*.py** - Platform-specific runners (78 platforms)
- **showet_api.py** - HTTP API for web-based access
- **showet-webui.py** - Convenience launcher for web UI

## Supported Platforms

| Category | Platforms |
|----------|-----------|
| **Commodore** | C64, C128, VIC20, Plus4, PET, Amiga, CBM-II |
| **Atari** | 2600, 5200, 7800, Jaguar, Lynx, ST/Falcon, XL/XE |
| **Nintendo** | NES, SNES, N64, GB, GBC, GBA, GameCube, Wii, 3DS, Pokémon Mini |
| **Sega** | Genesis, 32X, Saturn, Dreamcast, Game Gear, Master System, SG-1000, ST-V, VMU |
| **Sony** | PlayStation 1/2, PSP |
| **NEC** | PC-8800, PC-98, PC-FX, TurboGrafx, SuperGrafx |
| **Other** | MSX, MS-DOS, Windows (Wine), Oric, WebAssembly, Raspberry Pi, Apple II, ZX Spectrum |

See [Docs/platform-compatibility.md](Docs/platform-compatibility.md) for detailed emulator and extension mappings.

## Web UI

The web interface provides:
- Search demos on pouet.net
- Browse supported platforms
- Run demos directly from the browser

**API Endpoints:**
- `GET /api/platforms` - List all supported platforms
- `GET /api/search?q=...` - Search pouet.net productions
- `POST /api/run/{id}` - Launch a demo

See [Docs/API.md](Docs/API.md) for full API documentation.

## Development

Run tests:
```bash
python3 -m unittest discover -s tests
```

Build Debian package:
```bash
debuild -us -uc -b
```

## Documentation

- [API Documentation](Docs/API.md)
- [Platform Compatibility Matrix](Docs/platform-compatibility.md)
- [GUI Modernization Plan](Docs/GUI-modernization.md)

## Authors

- Code: Ville Ranki (Original Author 2004)
- Code: Bauke Molenaar (Since: 2022)
- Logo & Icon: Manu / Fit