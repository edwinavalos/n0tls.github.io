#!/usr/bin/env python3
"""
Watches posts/ for new or moved-in markdown files and auto-publishes to GitHub.
Run as a systemd user service.
"""

import logging
import subprocess
import sys
import threading
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

REPO_DIR = Path("/home/edwin/repos/n0tls.github.io")
POSTS_DIR = REPO_DIR / "posts"

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
    log.info(f"New post detected: {path.name}")
    try:
        git("pull", "--rebase", "origin", "main")
        git("add", str(path))
        # Nothing staged means the file was already committed somehow
        diff = git("diff", "--cached", "--name-only")
        if not diff:
            log.info(f"No changes staged for {path.name}, skipping commit")
            return
        git("commit", "-m", f"Add post: {path.stem}")
        git("push", "origin", "main")
        log.info(f"Published: {path.name}")
    except RuntimeError as e:
        log.error(f"Failed to publish {path.name}: {e}")


SETTLE_SECONDS = 10


class PostHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self._timers: dict[Path, threading.Timer] = {}
        self._lock = threading.Lock()

    def _schedule(self, path: Path):
        with self._lock:
            existing = self._timers.pop(path, None)
            if existing:
                existing.cancel()
            t = threading.Timer(SETTLE_SECONDS, publish, args=[path])
            self._timers[path] = t
            t.start()
        log.info(f"Waiting {SETTLE_SECONDS}s for {path.name} to settle...")

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix == ".md":
            self._schedule(path)

    def on_modified(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix == ".md":
            self._schedule(path)

    def on_moved(self, event):
        # Catches files moved/renamed into the posts/ directory
        if event.is_directory:
            return
        path = Path(event.dest_path)
        if path.suffix == ".md":
            self._schedule(path)


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
