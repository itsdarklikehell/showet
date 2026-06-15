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

## Phase 4: Documentation & Refactoring (In Progress)

**Goal:** Improve documentation, code quality, and add missing platform support.

Tasks:
*   **Task 4.1 (Documentation):** Create API documentation and platform compatibility matrix ✅
*   **Task 4.2 (Bug Fixes):** Fix platform runner issues (Windows path handling, C64 extensions) ✅
*   **Task 4.3 (Testing):** Expand test coverage for platform runners
*   **Task 4.4 (Missing Platforms):** Add support for Alambik, Flash/SWF (Ruffle), Android

---

## Notable Missing Platforms (from pouet.net)

Based on pouet.net platform listings, these platforms are not yet implemented:
- **Oric** - Oric-1/Atmos ✅ (added: `Platform_Tangerine_Oric.py`)
- **WebAssembly** - WASM/HTML5 demos ✅ (added: `Platform_WebAssembly_Web.py`)
- **Raspberry Pi** - Bare-metal Pi demos ✅ (added: `Platform_Raspberry_Pi.py`)

Legacy formats without clear emulation paths:
- **Alambik** - Proprietary Windows browser plugin (low priority)
- **Flash/SWF** - Could use Ruffle emulator
- **Android** - Would require Android emulator integration