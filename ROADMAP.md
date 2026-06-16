# Showet Modernization Roadmap

## 🗺️ Goal
Modernize Showet from a "collection of scripts" into a cohesive, scalable, production-ready demo runner with both CLI and browser-based playback.

## 🚀 Phase 1-3: Foundation & Integration - ✅ COMPLETE (2025-06-16)
*   **Core Definition:** `PlatformBase.py` abstract class with OOP contract
*   **Documentation:** `README.md`, `CONTRIBUTING.md` created
*   **Refactoring:** All 84 platform modules refactored to use `PlatformBase`
*   **nostalgist.js Integration:** 84 JSON configs + loader for TVS browser playback
*   **CI/CD:** GitHub Actions workflow, Docker support added
*   **Git:** Changes pushed to `origin/master` ✓

## ✨ Phase 4: Polish & Production Ready
*   **Build System:** Add Poetry for dependency management
*   **Testing:** Full pytest suite with coverage
*   **API Layer:** Update `showet_api.py` for PlatformBase
*   **Web UI:** Complete frontend with demo browser/search

## 💎 Phase 5: Future Features
*   Save-state management across platforms
*   Multiplayer/collaborative demo viewing
*   Streaming integration for live demos

---

## 🛠️ Action Items Status
| # | Task | Status |
|---|------|--------|
| 1 | PlatformBase.py | ✅ Complete |
| 2 | Platform refactoring | ✅ Complete |
| 3 | nostalgist.js bridge | ✅ Complete |
| 4 | CI/CD + Docker | ✅ Complete |
| 5 | Testing harness | 📋 TODO |
| 6 | API layer upgrade | 📋 TODO |

---

*This roadmap drives the "demo-runner of the future" vision. Next: polish the API and web UI!*