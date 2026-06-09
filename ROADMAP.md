# Project Roadmap: showet Modernization

This roadmap outlines the plan for modernizing the `showet` project, focusing on stability, feature implementation, and eventual architectural upgrades.

## Guiding Principles
*   **Preserve Behavior First:** Ensure that existing functionality remains correct during all modifications.
*   **Iterative Approach:** Tackle large goals in smaller, achievable phases.
*   **Stability over Speed:** Prioritize code quality and testing before feature implementation.

## Phase 1: Stabilization & Quality
**Goal:** Make the existing CLI tool robust, testable, and maintainable.
*   **Task 1.1 (Code Refactoring):** Deeply refactor `showet.py` to adhere to SOLID principles, making the platform runner detection and file handling logic cleaner and more modular.
*   **Task 1.2 (Testing Expansion):** Expand `tests/test_showet.py` to cover all modes of the dispatcher (platform listing, file handling success/failure paths).
*   **Task 1.3 (Documentation Review):** Ensure all internal documentation (`README.md`) accurately reflects the new, cleaner structure.

## Phase 2: Core Feature Implementation
**Goal:** Implement the core functionality of displaying/running a production based on the selected platform.
*   **Task 2.1 (Platform Hook):** Develop a concrete mechanism where the selected platform runner is actually invoked or configured based on the data downloaded. This connects the data to the actual retroarch experience.
*   **Task 2.2 (UI/UX Mockup):** Define a clear output format (e.g., a structured JSON output or an HTML/Canvas rendering) that the dispatcher will produce.

## Phase 3: Technology Modernization
**Goal:** Plan and execute a migration to a more modern, scalable architecture.
*   **Task 3.1 (Architecture Decision):** Decide on the new stack (e.g., moving from a monolithic CLI to a microservice, or using a modern frontend framework).
*   **Task 3.2 (Migration):** If a full rewrite is chosen, start building a Proof of Concept (PoC) for the new architecture using the stable core logic developed in Phase 1.

---
*This roadmap will be updated as we progress.*