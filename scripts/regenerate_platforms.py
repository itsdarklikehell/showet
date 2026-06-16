#!/usr/bin/env python3
"""Regenerate all Platform_*.py files with correct supported_platforms() method."""
import re
from pathlib import Path

# Read the original unmodified versions from git
import subprocess

project_root = Path(__file__).parent

# Get all platform files that need fixing
broken_files = []
for pf in sorted(project_root.glob("Platform_*.py")):
    content = pf.read_text()
    if "def supported_platforms" not in content and pf.name != "PlatformBase.py":
        broken_files.append(pf)

print(f"Found {len(broken_files)} files needing supported_platforms()")

for pf in broken_files[:3]:
    print(f"Sample: {pf.name}")