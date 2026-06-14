# GUI Modernization Plan

## Current State

The showet GUI uses Qt5/QML with the following components:

### Files
- `showet-gui/main.qml` - Main application window with TabView (Search/Browser)
- `showet-gui/SearchView.qml` - Search interface querying pouet.net API
- `showet-gui/BrowserView.qml` - Embedded pouet.net browser with "Run" button
- `showet-gui/Header.qml` - Search input header
- `showet-gui/ProdDelegate.qml` - List item delegate for search results
- `showet-gui/showethelper.cpp` - C++ backend for demo execution

### Technology Stack (Qt5)
- QtQuick 2.0
- QtQuick.Controls 1.4
- QtQuick.Layouts 1.2
- QtWebEngine 1.5

## Issues Identified

1. **Outdated Qt Version**: QtQuick 2.0/QtQuick.Controls 1.4 are from Qt5 era (2014). Current Qt6 uses QtQuick.Controls 2.x.

2. **Deprecated APIs**: `XMLHttpRequest` usage, `ListElement` patterns, and `onUrlChanged` signal handler patterns have evolved.

3. **Platform-Specific Backend**: The C++ helper requires compilation and doesn't work cross-platform without building.

4. **No Installation Method**: The QML files aren't integrated with the pyproject.toml build system.

## Modernization Options

### Option A: Qt6 Migration (Incremental)
- Update to QtQuick 2.15/QtQuick.Controls 2.x
- Replace XMLHttpRequest with Fetch/XHR from Qt.labs
- Use Qt Quick Controls Material or Universal style
- Update WebEngineView to Qt6 equivalent

**Pros:** Minimal changes, maintains native desktop UX
**Cons:** Still requires Qt installation, limited cross-platform support

### Option B: Web-Based UI (OpenClaw Canvas)
- Create a web-based UI that can be served via OpenClaw's canvas system
- Use modern web frameworks (React/Vue or vanilla JS)
- Integrate with showet Python backend via HTTP API

**Pros:** Cross-platform, no Qt dependencies, works in browser, easier styling
**Cons:** More development work, requires backend HTTP server

### Option C: TUI (Terminal UI)
- Use Textual or Rich library for modern terminal interface
- Works everywhere, no GUI dependencies

**Pros:** Universal compatibility, modern TUI experience
**Cons:** No visual appeal, different user experience

## Recommendation

**Hybrid approach:**
1. First, create a proof-of-concept web-based UI using the Canvas system
2. Maintain Qt GUI for desktop users who already have it
3. Add a `--tui` flag for terminal users

## Implementation Steps

### Step 1: Web API Endpoint
Expose the showet functionality via a local HTTP API:
- `GET /api/search?q=<query>&platform=<slug>` - Search pouet.net
- `POST /api/run/<pouetid>` - Run a demo (returns JSON status)
- `GET /api/platforms` - List supported platforms

### Step 2: Web UI Prototype
Create a simple HTML/JS interface:
- Search form with autocomplete
- Results list with thumbnails
- Run button that triggers backend execution

### Step 3: Canvas Integration
Host the web UI via OpenClaw canvas for in-browser access.