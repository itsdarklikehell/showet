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

## ✨ Phase 4: Polish & Production Ready - 🚧 IN PROGRESS (2026-06-17)
*   **Build System:** ✅ Add Poetry for dependency management
*   **Testing:** ✅ Full pytest suite with coverage expanded
*   **API Layer:** ✅ Update `showet_api.py` for PlatformBase + demo search
*   **Web UI:** ✅ Complete frontend with demo browser/search (showet-showcase.html)

### Phase 4 Tasks
| # | Task | Status |
|---|------|--------|
| 1 | Poetry configuration in pyproject.toml | ✅ Complete |
| 2 | Expanded test coverage for all modules | ✅ Complete |
| 3 | API layer with search and demo info | ✅ Complete |
| 4 | nostalgist.js server entrypoint | ✅ Complete |
| 5 | Run lint and verify test suite | 🚧 In Progress |

## 💎 Phase 5: Future Features
*   Save-state management across platforms
*   Multiplayer/collaborative demo viewing
*   **Streaming integration** ✅ COMPLETE
  - Twitch/YouTube/Facebook Live RTMP support
  - Local RTSP server for OBS capture
  - Webcam overlay support
  - Text overlays with demo info
  - Hardware encoder options

## 🎮 Phase 6: Demoscene Features (COMPLETE!)
*   **Demo Database:** Favorites, history, recommendations
*   **Party Calendar:** Upcoming demoparty integration
*   **CRT Presets:** Authentic retro shader configurations

---

## 🛠️ Action Items Status
| # | Task | Status |
|---|------|--------|
| 1 | PlatformBase.py | ✅ Complete |
| 2 | Platform refactoring | ✅ Complete |
| 3 | nostalgist.js bridge | ✅ Complete |
| 4 | CI/CD + Docker | ✅ Complete |
| 5 | Testing harness | ✅ Complete |
| 6 | API layer upgrade | ✅ Complete |
| 7 | Streaming integration | ✅ Complete |
| 8 | OBS integration | ✅ Complete |
| 9 | Chat overlay system | ✅ Complete |
| 10 | Demo scheduler/voting | ✅ Complete |
| 11 | CRT shader presets | ✅ Complete |
| 12 | Demo spotlight/hall of fame | ✅ Complete |

## 📊 Platform Audit (2025-06-16)
- **Total platforms**: 84
- **Working**: 84/84
- **Issues**: 0
- All platforms have functional `run()` method
- All platforms configured with cores and extensions
- Ready for streaming and nostalgist integration

---

*This roadmap drives the "demo-runner of the future" vision. Next: polish the API and web UI!*