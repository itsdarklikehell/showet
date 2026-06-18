#!/usr/bin/env python3
"""
TVS99 Setup Wizard - Configure Television Simulator '99 for Showet.

Provides step-by-step setup for browser-based demo playback.
"""

import json
from pathlib import Path
import subprocess
import sys


def check_nostalgist_config() -> bool:
    """Check if nostalgist configs exist."""
    config_dir = Path("nostalgist_configs")
    if not config_dir.exists():
        return False
    return any(config_dir.glob("*.json"))


def generate_configs() -> int:
    """Generate nostalgist configs for all platforms."""
    from nostalgist_bridge import generate_batch_configs
    return generate_batch_configs(Path("."), Path("nostalgist_configs"))


def check_http_server() -> bool:
    """Check if a local HTTP server can be started."""
    try:
        result = subprocess.run(["python3", "-m", "http.server", "--help"], 
                               capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False


def create_tvs99_readme() -> None:
    """Create README for TVS99 setup in the project."""
    readme_content = """# Television Simulator '99 Setup

This guide helps you configure the TVS99 browser-based demo player.

## Quick Start

```bash
# 1. Generate platform configs
python3 nostalgist_bridge.py

# 2. Generate manifest
python3 generate_manifest.py

# 3. Start HTTP server
python3 -m http.server 8000

# 4. Open in browser
# http://localhost:8000/showet-showcase.html
```

## Features

- **84+ Platform Support** - All Showet platforms available
- **CRT Authenticity** - Multiple shader options
- **Jukebox Mode** - Auto-advance with loop detection
- **Tour Player** - Guided demoscene history tour

## Configuration Files

| File | Purpose |
|------|---------|
| `nostalgist_configs/*.json` | Per-platform emulator configs |
| `nostalgist_configs/manifest.json` | Full platform index |
| `showet-showcase.html` | Main demo showcase interface |
| `showet-nostalgist-loader.js` | nostalgist.js integration |
| `showet-tour-player.js` | Historical tour mode |

## Controls

| Key | Action |
|-----|--------|
| 1-9 | Select platform/channel |
| Enter | Launch selected demo |
| F | Fullscreen mode |
| S | Shader selection menu |
| M | Mute/unmute audio |
| J | Toggle jukebox mode |
| T | Start tour mode |

## Jukebox Integration

The jukebox mode works in the browser:

```javascript
// Enable jukebox mode
showetNostalgist.setJukebox([
    {id: 12345, title: "Second Reality", platform: "commodore_64"},
    {id: 67890, title: "Heaven Seven", platform: "commodore_amiga"}
]);

// Start playback
showetNostalgist.startJukebox();
```

## Troubleshooting

1. **CORS errors** - Use HTTP server, not file://
2. **Missing cores** - Check RetroArch installation
3. **No audio** - Click inside browser window first
4. **Slow loading** - Reduce canvas resolution in config
"""
    
    Path("TVS99_SETUP.md").write_text(readme_content)


def main():
    """Run the TVS99 setup wizard."""
    print("📺 Television Simulator '99 Setup Wizard\n")
    print("=" * 40)
    
    # Check configs
    print("\n1. Checking nostalgist configs...")
    if check_nostalgist_config():
        print("   ✅ Configs exist")
    else:
        print("   ⚠ Generating configs...")
        try:
            count = generate_configs()
            print(f"   ✅ Generated {count} configs")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # Check HTTP server
    print("\n2. Checking HTTP server capability...")
    if check_http_server():
        print("   ✅ HTTP server available (python3 -m http.server)")
    else:
        print("   ❌ HTTP server not available")
    
    # Create setup readme
    print("\n3. Creating setup documentation...")
    create_tvs99_readme()
    print("   ✅ Created TVS99_SETUP.md")
    
    print("\n" + "=" * 40)
    print("\nTo start TVS99:")
    print("  python3 -m http.server 8000")
    print("  open http://localhost:8000/showet-showcase.html")
    print("\n🎮 Enjoy authentic demoscene in your browser!")


if __name__ == "__main__":
    main()