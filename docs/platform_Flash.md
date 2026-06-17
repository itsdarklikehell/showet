# Flash/SWF Platform Support

## Supported Emulators

```python
emulators = ['retroarch', 'ruffle']
```

## Supported Libretro Cores

```python
cores = ['ruffle_libretro']
```

## Supported File Extensions

```python
extensions = ['swf', 'spl']
```

## Installation

### Ruffle Standalone (Recommended)
```bash
# Ubuntu/Debian
sudo apt install ruffle

# Or download from https://ruffle.rs
```

### RetroArch Core
The `ruffle_libretro` core can be installed via RetroArch's core downloader.

## Usage

```bash
showet --platforms | grep -i flash
```

## Examples

### Flash Demo
Name: Whatever
By: Some Group
Type: demo
Platform: flash
`./showet.py <pouet_id>`

## Notes

- Ruffle focuses on AS1/2 compatibility with sandboxed playback
- Some Flash demos with advanced interactivity may not work fully
- The platform supports versions v1-v10 via different slugs