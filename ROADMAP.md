# Showet Modernization Roadmap

## 🗺️ Goal
The primary goal for the immediate future is to modernize the Showet framework from its current collection of platform-specific scripts into a cohesive, scalable, and maintainable product. This requires a shift from a "collection of scripts" approach to a structured, modern software architecture.

## 🚀 Phase 1: Stabilization and Core Definition (Short-Term: Next 1-2 Sprints) - ✅ COMPLETE
*   **Core Definition:** Define a standard, abstract interface/protocol for all platforms (`PlatformBase.py`). ✅ DONE - 2025-06-16
*   **Documentation Foundation:** Finalize `README.md` and create comprehensive `CONTRIBUTING.md`. ✅ DONE - 2025-06-16
*   **API Refinement:** Solidify `showet_api.py` as the *single source of truth* for platform interactions.
*   **Dependencies:** Review and consolidate external dependencies in `pyproject.toml`.

## ✨ Phase 2: Architectural Unification (Mid-Term: Next Quarter) - ✅ COMPLETE
*   **Modularization:** Refactor all `Platform_*.py` to inherit from `PlatformBase`. ✅ DONE - All 84 platforms refactored 2025-06-16
*   **Build System:** Standardize build system with Poetry/pytest. 🔄 IN PROGRESS
*   **Modernization:** Upgrade core infrastructure components.
*   **UI/UX Polish:** Focus on unified look and feel for `showet-gui/` and `showet-webui/`.

## 📺 Phase 3: nostalgist.js Integration (Added 2025-06-16) - ✅ COMPLETE
*   **Television Simulator Integration:** Clone available at `projects/nostalgist/`. ✅ DONE
*   **nostalgist.js Bridge:** `nostalgist_bridge.py` generates configs for all 84 platforms. ✅ DONE
*   **Config Generator:** 84 JSON configs in `nostalgist_configs/` ready for TVS playback. ✅ DONE

## 💎 Phase 4: Feature Expansion and Hardening (Long-Term)
*   **Testing Harness:** Create dedicated testing infrastructure.
*   **API Layer Upgrade:** Update `showet_api.py` to use new PlatformBase instances.
*   **Save-State Management:** Implement unified save/load across platforms.
*   **Community & Governance:** Establish formal contribution model.

## 🛠️ Action Items
1.  ✅ **COMPLETE** - PlatformBase.py abstract class/interface
2.  ✅ **COMPLETE** - Contribute.md documentation
3.  ✅ **COMPLETE** - All 84 platform modules refactored
4.  ✅ **COMPLETE** - nostalgist_bridge.py config generator
5.  [ ] 🔄 Build system integration (Poetry/pytest)
6.  [ ] Testing harness creation
7.  [ ] Update showet_api.py for PlatformBase

### 📊 Progress Summary
| Task | Status | Date |
|------|--------|------|
| PlatformBase.py created | ✅ | 2025-06-16 |
| Automation script created | ✅ | 2025-06-16 |
| All platforms refactored | ✅ | 2025-06-16 |
| nostalgist.js integration | ✅ | 2025-06-16 |
| Testing harness | ⏳ | Pending |
| API layer upgrade | 📋 | TODO |

*This roadmap is a living document and will be updated as development progresses.*