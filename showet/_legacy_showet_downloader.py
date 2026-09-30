#!/usr/bin/env python3
"""Showet downloader module.

Handles production metadata and file downloads from pouet.net, scene.org, and modarchive.org.
"""

from __future__ import annotations

import json
import logging
import subprocess
import urllib.request
from pathlib import Path
from typing import Any

from showet._legacy_showet_config import CACHE_DIR, DEBUG

logger = logging.getLogger("showet.downloader")


def download_production_json(prod_id: int, cache_dir: Path | None = None) -> dict[str, Any]:
    """Download JSON metadata for a production, caching it locally.
    
    Args:
        prod_id: Pouet.net production ID
        cache_dir: Optional custom cache directory
        
    Returns:
        Parsed JSON metadata dict
        
    Raises:
        RuntimeError: If download fails
    """
    if cache_dir is None:
        cache_dir = CACHE_DIR / str(prod_id)

    cache_dir.mkdir(parents=True, exist_ok=True)
    json_path = cache_dir / "pouet.json"

    if json_path.exists() and DEBUG:
        logger.debug("Loading cached JSON for production %d", prod_id)
        return json.loads(json_path.read_text())

    url = f"http://api.pouet.net/v1/prod/?id={prod_id}"
    logger.info("Downloading metadata for production %d from %s", prod_id, url)

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            json_str = response.read().decode()
        json_path.write_text(json_str)
        if DEBUG:
            logger.debug("Cached JSON to %s", json_path)
        return json.loads(json_str)
    except urllib.error.URLError as e:
        logger.error("Failed to download production %d: %s", prod_id, e)
        raise RuntimeError(f"Error downloading production {prod_id}: {e}") from e


def download_production_file(data: dict[str, Any], datadir: Path) -> Path:
    """Download the production file if missing.

    Args:
        data: Production metadata dict from pouet.net API
        datadir: Directory to download files to

    Returns:
        The data directory path

    Raises:
        RuntimeError: If download fails
    """
    download_url = data["prod"]["download"].replace(
        "https://files.scene.org/view", "https://files.scene.org/get"
    )

    flag_file = datadir / ".FILES_DOWNLOADED"
    if flag_file.exists():
        if DEBUG:
            logger.debug("Production files already downloaded")
        return datadir

    logger.info("Downloading production file from %s", download_url)

    try:
        with urllib.request.urlopen(download_url, timeout=120) as response:
            filename = response.url.split("/")[-1]
            if not filename:
                raise RuntimeError(f"Error downloading file at {download_url}")

            dest = datadir / filename
            dest.write_bytes(response.read())

            if DEBUG:
                logger.debug("Downloaded: %s (%d bytes)", dest, dest.stat().st_size)

            # Unpack archives if needed
            _unpack_archive(dest, datadir)

            flag_file.touch()
            return datadir
    except urllib.error.URLError as e:
        logger.error("Failed to download production file: %s", e)
        raise RuntimeError(f"Error downloading file at {download_url}: {e}") from e


def _unpack_archive(archive_path: Path, dest_dir: Path) -> None:
    """Unpack a downloaded archive into dest_dir if it is a supported type."""
    ext = archive_path.suffix.lower()
    handlers = {
        ".zip": ["unzip", "-o", "-d", str(dest_dir), str(archive_path)],
        ".rar": ["unrar", "x", "-o+", str(archive_path), str(dest_dir) + "/"],
        ".7z": ["7z", "x", str(archive_path), f"-o{dest_dir}"],
        ".lha": ["lha", "xw=" + str(dest_dir), str(archive_path)],
        ".tar": ["tar", "xf", str(archive_path), "-C", str(dest_dir)],
        ".gz": ["tar", "xzf", str(archive_path), "-C", str(dest_dir)],
        ".xz": ["tar", "xf", str(archive_path), "-C", str(dest_dir)],
        ".bz2": ["tar", "xjf", str(archive_path), "-C", str(dest_dir)],
    }

    if ext not in handlers:
        return  # Not an archive we know how to unpack

    # Clean up the original archive after unpacking
    try:
        import shutil
        logger.info("Unpacking %s into %s", archive_path.name, dest_dir)
        cmd = handlers[ext]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            logger.warning("Unpack command failed for %s: %s", archive_path, result.stderr)
        else:
            archive_path.unlink()
            if DEBUG:
                logger.debug("Unpacked and removed: %s", archive_path.name)
    except FileNotFoundError:
        logger.warning("Unpack tool not found for %s extension", ext)
    except Exception as e:
        logger.warning("Failed to unpack %s: %s", archive_path, e)


def get_random_production_id() -> int:
    """Get a random production ID from pouet.net.
    
    Returns:
        Production ID or -1 if failed
    """
    import random

    random_terms = ["demo", "intro", "64k", "4k", "music", "animation"]
    query = random.choice(random_terms)
    url = f"http://api.pouet.net/v1/search/prod/?q={query}"

    logger.debug("Fetching random production with query: %s", query)

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())

        if data.get("success") and data.get("results"):
            results = list(data["results"].items())
            if results:
                prod_id, _ = random.choice(results)
                logger.info("Randomly selected production ID: %d", prod_id)
                return prod_id
    except Exception as e:
        logger.error("Failed to get random production: %s", e)

    return -1
