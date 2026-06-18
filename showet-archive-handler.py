#!/usr/bin/env python3
"""Showet Archive Handler - Extract demoscene archives for automatic execution."""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path


class ArchiveHandler:
    """Handles extraction of common demoscene archive formats."""
    
    def __init__(self, work_dir=None):
        self.work_dir = Path(work_dir or tempfile.mkdtemp(prefix="showet_demo_"))
        self.work_dir.mkdir(parents=True, exist_ok=True)
    
    def extract(self, archive_path, password=None):
        """Extract archive and return list of extracted files."""
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
    
    def _extract_zip(self, archive, password=None):
        """Extract ZIP archive."""
        try:
            cmd = ['unzip', '-o', str(archive), '-d', str(self.work_dir)]
            if password:
                cmd.extend(['-P', password])
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError as e:
            print(f"ZIP extraction failed: {e.stderr}")
            return None
    
    def _extract_rar(self, archive, password=None):
        """Extract RAR archive."""
        try:
            cmd = ['unrar', 'x', '-o+', str(archive), str(self.work_dir) + '/']
            if password:
                cmd.extend(['-p' + password])
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError as e:
            print(f"RAR extraction failed: {e.stderr}")
            return None
    
    def _extract_7z(self, archive, password=None):
        """Extract 7z archive."""
        try:
            cmd = ['7z', 'x', str(archive), f'-o{self.work_dir}']
            if password:
                cmd.append(f'-p{password}')
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError as e:
            print(f"7z extraction failed: {e.stderr}")
            return None
    
    def _extract_lha(self, archive, password=None):
        """Extract LHA/LZH archive (common for Amiga/PC-98 demos)."""
        try:
            cmd = ['lha', 'x', str(archive), str(self.work_dir) + '/']
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError as e:
            print(f"LHA extraction failed: {e.stderr}")
            return None
    
    def cleanup(self):
        """Remove extracted files."""
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)


def main():
    if len(sys.argv) < 2:
        print("Usage: showet-archive <archive_path> [--password PASS] [--list]")
        print("\nSupported formats: .zip, .rar, .7z, .lha, .lzh")
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
        if arg == '--list':
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
    else:
        print("Extraction failed or unsupported format")
        sys.exit(1)


if __name__ == '__main__':
    main()