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