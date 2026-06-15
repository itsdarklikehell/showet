# Project Roadmap: showet Modernization

This roadmap outlines the plan for modernizing the `showet` project, focusing on stability, feature implementation, and eventual architectural upgrades.

## Guiding Principles
*   **Preserve Behavior First:** Ensure that existing functionality remains correct during all modifications.
*   **Iterative Approach:** Tackle large goals in smaller, achievable phases.
*   **Stability over Speed:** Prioritize code quality and testing before feature implementation.

## Phase 1: Stabilization & Quality ✅
**Goal:** Make the existing CLI tool robust, testable, and maintainable.

Completed Tasks:
*   **Task 1.0 (Bug Fix):** Fixed syntax error in Platform_Commodore_64.py (missing comma in list).
*   **Task 1.1 (Interface Unification):** Refactored 4 platform stubs to inherit from PlatformCommon consistently (Platform_Commodore_Amiga, Platform_Amstrad_Cpcplus, Platform_Apple_AppleII, Platform_Apple_AppleI, Platform_Apple_AppleIIGS).
*   **Task 1.2 (Testing Expansion):** Added 8 unit tests covering platform selection logic and run_production error paths.

Remaining:
*   **Task 1.3 (Documentation Review):** Ensure all internal documentation (`README.md`) accurately reflects the new, cleaner structure.

## Phase 2: Core Feature Implementation ✅
**Goal:** Implement the core functionality of displaying/running a production based on the selected platform.

Completed Tasks:
*   **Task 2.1 (Platform Hook):** Refactored PlatformCommon base class and platform runners (C64, PSX) with cleaner interface, proper type hints, and reliable file discovery using os.walk.
*   **Task 2.2 (UI/UX Mockup):** Created `Docs/GUI-modernization.md` documenting Qt5/QML architecture and proposed modernization options (Qt6 migration, web-based UI via Canvas, TUI).

## Phase 3: Technology Modernization ✅
**Goal:** Complete refactoring and build web-based UI Proof of Concept.

Completed Tasks:
*   **Task 3.0 (Platform Refactoring):** Refactored 69 platform runner files with clean template. All 78 Platform files now compile successfully.
*   **Task 3.1 (Web API):** Created `showet_api.py` with HTTP endpoints `/api/platforms`, `/api/search`, `/api/run/<id>`, and static file serving.
*   **Task 3.2 (Web UI PoC):** Created `showet-ui/index.html` with modern responsive design for demo browsing.

---
*This roadmap will be updated as we progress.*

## Phase 4: Documentation & Refactoring ✅

**Goal:** Improve documentation, code quality, and add missing platform support.

Completed Tasks:
*   **Task 4.1 (Documentation):** Create API documentation and platform compatibility matrix ✅
*   **Task 4.2 (Bug Fixes):** Fix platform runner issues (Windows path handling, C64 extensions) ✅
*   **Task 4.3 (Testing):** Expand test coverage for platform runners (14 tests passing) ✅

---

## Phase 5: Missing Platforms & Feature Enhancement (Planned)

**Goal:** Add platform support for Alambik, Flash/SWF, and Android.

Planned Tasks:
*   **Task 5.1 (Flash/SWF):** Add `Platform_Flash_Ruffle.py` using Ruffle emulator
*   **Task 5.2 (Android):** Add `Platform_Android_Android.py` using Android emulator
*   **Task 5.3 (Alambik):** Research and add platform support (low priority)

---

## Phase 6: Feature Polish (Planned)

**Goal:** Enhance user experience and add advanced features.

Planned Tasks:
*   **Task 6.1 (Demo Previews):** Add screenshot/thumbnail support to web UI
*   **Task 6.2 (Playlist Support):** Support multi-disk demos via M3U playlists
*   **Task 6.3 (Core Selection):** Allow users to choose which RetroArch core to use
*   **Task 6.4 (Fullscreen Options):** Add `--fullscreen`, `--audio` CLI flags
*   **Task 6.5 (Offline Mode):** Cache demos locally for offline playback

---

## Phase 7: RetroPie Integration (Planned)

**Goal:** Make showet work on RetroPie/Batocera/Raspberry Pi.

Planned Tasks:
*   **Task 7.1 (RetroPie Setup):** Create RetroPie menu integration scripts
*   **Task 7.2 (Pi Optimization):** Optimize for Raspberry Pi hardware
*   **Task 7.3 (Controller Support):** Add gamepad navigation to web UI