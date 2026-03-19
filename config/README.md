# Local machine config

These files need to be applied manually when setting up on a new machine.

## vimrc

Adds a blog post skeleton that auto-fills YAML front matter when you open a
new `.md` file inside `posts/` or `drafts/`.

To install, append it to your `~/.vimrc`:

```bash
cat config/vimrc >> ~/.vimrc
```

Or if you have no `~/.vimrc` yet:

```bash
cp config/vimrc ~/.vimrc
```

## autopublish.py

The repo root contains `autopublish.py`, a systemd user service that watches
`posts/` and auto-commits + pushes any new or modified markdown file.

To install on a new Linux machine:

```bash
# Install dependencies
pip install watchdog

# Copy and enable the systemd service
cp config/autopublish.service ~/.config/systemd/user/autopublish.service
systemctl --user daemon-reload
systemctl --user enable --now autopublish
```

> Note: `autopublish.py` hardcodes `REPO_DIR = Path("/home/edwin/repos/n0tls.github.io")`.
> Update that path if your home directory differs.
