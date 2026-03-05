#!/usr/bin/env python3
"""
Watches posts/ for new or moved-in markdown files and auto-publishes to GitHub.
Run as a systemd user service.
"""

import logging
import subprocess
import sys
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


class PostHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix == ".md":
            publish(path)

    def on_moved(self, event):
        # Catches files moved/renamed into the posts/ directory
        if event.is_directory:
            return
        path = Path(event.dest_path)
        if path.suffix == ".md":
            publish(path)


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
