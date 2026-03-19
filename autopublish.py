#!/usr/bin/env python3
"""
Watches posts/ for markdown file changes and auto-publishes to GitHub.

Vim-aware: waits for the swap file to be deleted (i.e. vim closed the file)
before publishing. For all other editors, falls back to a 10-second debounce
on the last write.

Run as a systemd user service (Linux) or launchd Launch Agent (macOS).
"""

from __future__ import annotations

import logging
import subprocess
import sys
import threading
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

REPO_DIR = Path(__file__).resolve().parent
POSTS_DIR = REPO_DIR / "posts"

# Delay after vim exits before publishing (short, just to let the OS settle)
VIM_CLOSE_DELAY = 2
# Delay after last write for non-vim editors
SETTLE_SECONDS = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def publish(path: Path):
    log.info(f"Publishing {path.name}...")
    try:
        # --autostash handles any other uncommitted changes in the working tree
        git("pull", "--rebase", "--autostash", "origin", "main")
        git("add", str(path))
        diff = git("diff", "--cached", "--name-only")
        if not diff:
            log.info(f"No changes in {path.name}, skipping commit")
            return
        git("commit", "-m", f"Add post: {path.stem}")
        git("push", "origin", "main")
        log.info(f"Published: {path.name}")
    except RuntimeError as e:
        log.error(f"Failed to publish {path.name}: {e}")


def publish_rename(old_path: Path, new_path: Path):
    log.info(f"Publishing rename {old_path.name} -> {new_path.name}...")
    try:
        git("pull", "--rebase", "--autostash", "origin", "main")
        # git add on a missing file stages its deletion; on the new file stages addition
        git("add", str(old_path), str(new_path))
        diff = git("diff", "--cached", "--name-only")
        if not diff:
            log.info("No changes staged, skipping commit")
            return
        git("commit", "-m", f"Rename post: {old_path.stem} -> {new_path.stem}")
        git("push", "origin", "main")
        log.info(f"Published rename: {new_path.name}")
    except RuntimeError as e:
        log.error(f"Failed to publish rename: {e}")


def swp_for(md_path: Path) -> Path:
    """Return the vim swap file path for a given .md file."""
    return md_path.parent / f".{md_path.name}.swp"


def md_for_swp(swp_path: Path) -> Path | None:
    """Derive the .md path from a vim swap file path, or None if not a match."""
    name = swp_path.name
    if name.startswith(".") and name.endswith(".swp"):
        md_name = name[1:-4]  # strip leading '.' and trailing '.swp'
        if md_name.endswith(".md"):
            return swp_path.parent / md_name
    return None


class PostHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self._timers: dict[Path, threading.Timer] = {}
        self._lock = threading.Lock()

    def _schedule(self, path: Path, delay: float):
        with self._lock:
            existing = self._timers.pop(path, None)
            if existing:
                existing.cancel()
            t = threading.Timer(delay, publish, args=[path])
            self._timers[path] = t
            t.start()
        log.info(f"Scheduling {path.name} in {delay:.0f}s...")

    def _cancel(self, path: Path):
        with self._lock:
            existing = self._timers.pop(path, None)
            if existing:
                existing.cancel()

    def on_deleted(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        # Swap file deleted = vim exited cleanly
        md_path = md_for_swp(path)
        if md_path and md_path.exists():
            log.info(f"Vim closed {md_path.name}")
            self._schedule(md_path, VIM_CLOSE_DELAY)

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix != ".md":
            return
        if swp_for(path).exists():
            # Vim opened this file — wait for swap deletion instead
            log.info(f"Vim has {path.name} open, waiting for close...")
            return
        self._schedule(path, SETTLE_SECONDS)

    def on_modified(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix != ".md":
            return
        if swp_for(path).exists():
            # Vim is still editing — reset any pending non-vim timer and wait
            self._cancel(path)
            return
        self._schedule(path, SETTLE_SECONDS)

    def on_moved(self, event):
        if event.is_directory:
            return
        old_path = Path(event.src_path)
        new_path = Path(event.dest_path)

        if new_path.suffix != ".md":
            return

        if swp_for(new_path).exists():
            log.info(f"Vim has {new_path.name} open, waiting for close...")
            return

        # Rename within posts/ — must stage the deletion of the old name too
        if old_path.parent == POSTS_DIR and old_path.suffix == ".md":
            log.info(f"Rename detected: {old_path.name} -> {new_path.name}")
            t = threading.Timer(VIM_CLOSE_DELAY, publish_rename, args=[old_path, new_path])
            t.start()
        else:
            # File moved in from outside posts/ — treat as new file
            self._schedule(new_path, SETTLE_SECONDS)


if __name__ == "__main__":
    log.info(f"Watching {POSTS_DIR} for new posts...")
    observer = Observer()
    observer.schedule(PostHandler(), str(POSTS_DIR), recursive=False)
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
