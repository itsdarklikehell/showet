"""
Pytest configuration and shared fixtures for Showet tests.
"""

import sys
from pathlib import Path
from unittest import mock

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def project_root():
    """Project root directory path."""
    return PROJECT_ROOT


@pytest.fixture
def mock_inquirer():
    """Mock the inquirer module."""
    return mock.MagicMock()


@pytest.fixture
def mock_patoolib():
    """Mock the patoolib module."""
    return mock.MagicMock()


@pytest.fixture(autouse=True)
def mock_external_deps(mock_inquirer, mock_patoolib):
    """Automatically mock external dependencies for all tests."""
    sys.modules["inquirer"] = mock_inquirer
    sys.modules["patoolib"] = mock_patoolib
    yield
    # Cleanup after test
    if "inquirer" in sys.modules:
        del sys.modules["inquirer"]
    if "patoolib" in sys.modules:
        del sys.modules["patoolib"]