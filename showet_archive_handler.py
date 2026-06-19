#!/usr/bin/env python3
"""Showet Archive Handler - Extract demoscene archives for automatic execution.

Handles extraction of ZIP, RAR, 7z, and LHA archives with password support.
Auto-detects archive type and extracts to temporary working directory.

Usage:
    showet-archive <archive_path> [--password PASS] [--list]
    showet-archive-handler <archive_path> [--list]
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Archive handler commands
ARCHIVE_COMMANDS = {
    '.zip': ['unzip', '-o'],
    '.rar': ['unrar', 'x', '-o+'],
    '.7z': ['7z', 'x'],
    '.lha': ['lha', 'x'],
    '.lzh': ['lha', 'x'],
}


class ArchiveHandler:
    """Handles extraction of common demoscene archive formats."""
    
    def __init__(self, work_dir: str | None = None):
        """Initialize archive handler with working directory."""
        self.work_dir = Path(work_dir or tempfile.mkdtemp(prefix="showet_demo_"))
        self.work_dir.mkdir(parents=True, exist_ok=True)
    
    def extract(self, archive_path: str, password: str | None = None) -> list[Path] | None:
        """Extract archive and return list of extracted files.
        
        Args:
            archive_path: Path to the archive file
            password: Optional password for encrypted archives
            
        Returns:
            List of extracted file paths, or None on failure
        """
        archive = Path(archive_path)
        ext = archive.suffix.lower()
        
        if ext == '.zip':
            return self._extract_zip(archive, password)
        elif ext == '.rar':
            return self._extract_rar(archive, password)
        elif ext == '.7z':
            return self._extract_7z(archive, password)
        elif ext in ['.lha', '.lzh']:
            return self._extract_lha(archive, password)
        else:
            return None
    
    def _extract_zip(self, archive: Path, password: str | None = None) -> list[Path] | None:
        """Extract ZIP archive."""
        try:
            cmd = ARCHIVE_COMMANDS['.zip'] + [str(archive), '-d', str(self.work_dir)]
            if password:
                cmd.extend(['-P', password])
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError as e:
            print(f"ZIP extraction failed: {e.stderr}")
            return None
    
    def _extract_rar(self, archive: Path, password: str | None = None) -> list[Path] | None:
        """Extract RAR archive."""
        try:
            cmd = ARCHIVE_COMMANDS['.rar'].copy()
            cmd.extend([str(archive), str(self.work_dir) + '/'])
            if password:
                cmd.extend(['-p' + password])
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError as e:
            print(f"RAR extraction failed: {e.stderr}")
            return None
    
    def _extract_7z(self, archive: Path, password: str | None = None) -> list[Path] | None:
        """Extract 7z archive."""
        try:
            cmd = ARCHIVE_COMMANDS['.7z'].copy()
            cmd.extend([str(archive), f'-o{self.work_dir}'])
            if password:
                cmd.append(f'-p{password}')
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError as e:
            print(f"7z extraction failed: {e.stderr}")
            return None
    
    def _extract_lha(self, archive: Path, password: str | None = None) -> list[Path] | None:
        """Extract LHA/LZH archive (common for Amiga/PC-98 demos)."""
        try:
            cmd = ARCHIVE_COMMANDS['.lha'].copy()
            cmd.extend([str(archive), str(self.work_dir) + '/'])
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError as e:
            print(f"LHA extraction failed: {e.stderr}")
            return None
    
    def cleanup(self) -> None:
        """Remove extracted files."""
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: showet-archive <archive_path> [--password PASS] [--list]")
        print("\nSupported formats: .zip, .rar, .7z, .lha, .lzh")
        print("\nOptions:")
        print("  --password PASS  Password for encrypted archives")
        print("  --list           List extracted files")
        sys.exit(1)
    
    archive_path = sys.argv[1]
    password = None
    list_only = False
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--password' and i + 1 < len(sys.argv):
            password = sys.argv[i + 1]
            i += 1
        elif arg == '--list':
            list_only = True
        i += 1
    
    handler = ArchiveHandler()
    files = handler.extract(archive_path, password)
    
    if files:
        print(f"Extracted {len(files)} files to {handler.work_dir}")
        if list_only:
            for f in files[:20]:  # Show first 20
                print(f"  {f.relative_to(handler.work_dir)}")
            if len(files) > 20:
                print(f"  ... and {len(files) - 20} more")
        return 0
    else:
        print("Extraction failed or unsupported format")
        sys.exit(1)


if __name__ == '__main__':
    main()