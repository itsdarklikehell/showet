#!/usr/bin/env python3
"""Bulk fix all Platform_*.py files to add supported_platforms() method."""
from pathlib import Path
import re

project_root = Path(__file__).parent

fixed = 0
for pf in sorted(project_root.glob("Platform_*.py")):
    if pf.name == "PlatformBase.py":
        continue
    
    content = pf.read_text()
    
    if "def supported_platforms" in content:
        continue
    
    # Extract slug from __init__
    slug_match = re.search(r'super\(\).__init__\("([^"]+)"', content)
    if slug_match:
        slug = slug_match.group(1)
        
        # Find where to insert - after extensions line
        lines = content.split('\n')
        insert_idx = None
        
        for i, line in enumerate(lines):
            if 'self.extensions = ' in line:
                insert_idx = i + 1
                break
        
        if insert_idx:
            # Build new content
            new_lines = lines[:insert_idx] + [
                '',
                '    def supported_platforms(self) -> list[str]:',
                f'        """Return the platform slug(s) this runner supports."""',
                f'        return ["{slug}"]'
            ] + lines[insert_idx:]
            
            pf.write_text('\n'.join(new_lines))
            fixed += 1
            print(f"✅ Fixed: {pf.name}")

print(f"\n✅ Total fixed: {fixed}")