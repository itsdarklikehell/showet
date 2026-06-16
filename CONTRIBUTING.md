# Contributing to Showet

Thank you for your interest in contributing to Showet! This document provides guidelines and standards for contributing to the project.

## 🏗️ Architecture Overview

Showet uses a modular OOP architecture where each platform emulator inherits from the `PlatformBase` abstract class.

### Key Components
- **`PlatformBase.py`** - Abstract base class defining the contract all platforms must implement
- **`platformcommon.py`** - Legacy common functionality (being integrated into PlatformBase)
- **`showet_api.py`** - Public API layer for programmatic access
- **`showet-gui/`** - Graphical user interface
- **`Platform_*.py`** - Individual platform implementations (84 total)

### Platform Implementation Contract
All platform modules must implement these abstract methods:
```python
def initialize(self) -> bool
def load_game(self, rom_path: str) -> bool  
def run_frame(self, controls: Dict[str, Any]) -> bool
def get_status_report(self) -> Dict[str, Any]
def save_state(self) -> bytes
def load_state(self, state_data: bytes) -> bool
```

## 🔧 Development Setup

### Requirements
- Python 3.10+
- RetroArch with appropriate cores installed

### Installation
```bash
pip install -e .
```

## 📏 Coding Standards

### Style
- Follow PEP 8 guidelines
- Use type hints for all public methods
- Document all methods with docstrings
- Use snake_case for variables, PascalCase for classes

### Linting
We use `ruff` for code quality:
```bash
ruff check .
ruff format .
```

## 🆕 Adding a New Platform

### Automated Path
Use the refactoring script to generate a template:
```bash
python3 scripts/refactor_platforms.py --platform Vendor_PlatformName
```

### Manual Steps
1. Create `Platform_Vendor_PlatformName.py`
2. Inherit from `PlatformBase`
3. Implement all 6 abstract methods
4. Add platform to API registry in `showet_api.py`
5. Update `ROADMAP.md` if needed

### Example Template
```python
from typing import Dict, Any
from PlatformBase import PlatformBase

class Platform_Nintendo_Switch(PlatformBase):
    def __init__(self):
        super().__init__("switch", version="1.0.0")
        # Set your platform-specific attributes here
        
    def initialize(self) -> bool:
        # Setup logic
        return True
        
    def load_game(self, rom_path: str) -> bool:
        # ROM loading logic
        return True
        
    # ... implement other abstract methods
```

## 🧪 Testing

- Add integration tests in `tests/`
- Test against actual ROM files where possible
- Verify RetroArch core compatibility

## 📦 Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-platform`)
3. Make changes and commit (`git commit -m 'Add Amazing Platform support'`)
4. Push to branch (`git push origin feature/amazing-platform`)
5. Open a Pull Request

## 📞 Questions?

Open an issue on GitHub for discussion.

---
*Last updated: 2025-06-16 (Phase 1 modernization)*