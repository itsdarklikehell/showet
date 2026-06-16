#!/usr/bin/env python3
"""Fix all Platform_*.py files to add supported_platforms() method."""
import re
from pathlib import Path

project_root = Path(__file__).parent

fixed_count = 0
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
        
        # Find extensions line and insert after it
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'self.extensions = ' in line:
                # Insert after this line
                lines.insert(i + 1, '')
                lines.insert(i + 2, '    def supported_platforms(self) -> list[str]:')
                lines.insert(i + 3, f'        """Return the platform slug(s) this runner supports."""')
                lines.insert(i + 4, f'        return ["{slug}"]')
                break
        
        pf.write_text('\n'.join(lines))
        fixed_count += 1
        print(f"✅ Fixed: {pf.name}")

print(f"\n✅ Total fixed: {fixed_count}")