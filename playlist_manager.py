"""Playlist handler for multi-disk demos.

Support for .m3u and .m3u8 playlist files used by multi-disk demos.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterator


class PlaylistManager:
    """Manages M3U/M3U8 playlist files for multi-disk demos."""

    @staticmethod
    def load_playlist(playlist_path: Path) -> list[Path]:
        """Load a playlist file and return list of referenced files.

        Args:
            playlist_path: Path to .m3u or .m3u8 file

        Returns:
            List of Path objects to the disk/image files
        """
        entries = []

        if not playlist_path.exists():
            return entries

        content = playlist_path.read_text(encoding="utf-8")

        for line in content.splitlines():
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            entry_path = playlist_path.parent / line
            if entry_path.exists():
                entries.append(entry_path)

        return entries

    @staticmethod
    def create_playlist(files: list[Path], output_path: Path) -> None:
        """Create a playlist file from a list of files.

        Args:
            files: List of file paths to include in playlist
            output_path: Where to write the .m3u file
        """
        lines = [str(f.name) for f in files]
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def find_playlists(directory: Path) -> list[Path]:
        """Find all playlist files in a directory.

        Args:
            directory: Directory to search

        Returns:
            List of .m3u and .m3u8 files found
        """
        playlists = []
        for pattern in ["*.m3u", "*.m3u8"]:
            playlists.extend(directory.glob(pattern))
        return sorted(playlists)

    @staticmethod
    def get_first_track(playlist_path: Path) -> Path | None:
        """Get the first track from a playlist.

        Args:
            playlist_path: Path to playlist file

        Returns:
            Path to first file, or None if playlist empty
        """
        entries = PlaylistManager.load_playlist(playlist_path)
        return entries[0] if entries else None

    @staticmethod
    def iter_by_rotation(entries: list[Path]) -> Iterator[tuple[int, Path]]:
        """Iterate over playlist entries with rotation index.

        Useful for demos that require disk swapping.

        Args:
            entries: List of file paths in playlist

        Yields:
            Tuples of (index, file_path) for each track
        """
        for i, entry in enumerate(entries):
            yield i, entry

    @staticmethod
    def detect_platform_from_playlist(playlist_path: Path) -> str | None:
        """Detect which platform a playlist belongs to based on extensions.

        Args:
            playlist_path: Path to playlist file

        Returns:
            Platform slug or None if unknown
        """
        extension_map = {
            ".adf": "commodore_amiga",
            ".dms": "commodore_amiga",
            ".ips": "commodore_amiga",
            ".dsk": "microsoft_msx",
            ".tap": "zx_spectrum",
            ".tzx": "zx_spectrum",
            ".cue": "sony_psx",
            ".ccd": "sony_psx",
            ".iso": "sony_psx",
        }

        entries = PlaylistManager.load_playlist(playlist_path)
        if not entries:
            return None

        # Check extensions of all entries
        for entry in entries:
            ext = entry.suffix.lower()
            if ext in extension_map:
                return extension_map[ext]

        return None