"""Archive handler module for Showet.

Extracts demoscene archives (ZIP, RAR, 7z, LHA) automatically.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

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
        self.work_dir = Path(work_dir or tempfile.mkdtemp(prefix="showet_demo_"))
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, archive_path: str, password: str | None = None) -> list[Path] | None:
        """Extract archive and return list of extracted files."""
        archive = Path(archive_path)
        ext = archive.suffix.lower()
        
        extractors = {
            '.zip': lambda: self._extract_zip(archive, password),
            '.rar': lambda: self._extract_rar(archive, password),
            '.7z': lambda: self._extract_7z(archive, password),
        }
        
        if ext in extractors:
            return extractors[ext]()
        return None

    def _extract_zip(self, archive: Path, password: str | None = None) -> list[Path] | None:
        try:
            cmd = ARCHIVE_COMMANDS['.zip'] + [str(archive), '-d', str(self.work_dir)]
            if password:
                cmd.extend(['-P', password])
            subprocess.run(cmd, check=True, capture_output=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError:
            return None

    def _extract_rar(self, archive: Path, password: str | None = None) -> list[Path] | None:
        try:
            cmd = ARCHIVE_COMMANDS['.rar'].copy()
            cmd.extend([str(archive), f"{self.work_dir}/"])
            subprocess.run(cmd, check=True, capture_output=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError:
            return None

    def _extract_7z(self, archive: Path, password: str | None = None) -> list[Path] | None:
        try:
            cmd = ARCHIVE_COMMANDS['.7z'].copy()
            cmd.extend([str(archive), f'-o{self.work_dir}'])
            if password:
                cmd.append(f'-p{password}')
            subprocess.run(cmd, check=True, capture_output=True)
            return list(self.work_dir.rglob('*'))
        except subprocess.CalledProcessError:
            return None

    def cleanup(self) -> None:
        """Remove extracted files."""
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)