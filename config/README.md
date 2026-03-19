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

The repo root contains `autopublish.py`, which watches `posts/` and
auto-commits + pushes any new or modified markdown file. It detects its own
location so no path changes are needed.

### macOS (launchd)

```bash
# Install dependencies
pip3 install watchdog

# Install and load the Launch Agent
cp config/com.n0tls.autopublish.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.n0tls.autopublish.plist
```

To check it's running:

```bash
launchctl list | grep autopublish
```

Logs go to `/tmp/autopublish.log`.

To stop/restart:

```bash
launchctl unload ~/Library/LaunchAgents/com.n0tls.autopublish.plist
launchctl load   ~/Library/LaunchAgents/com.n0tls.autopublish.plist
```

### Linux (systemd)

```bash
# Install dependencies
pip install watchdog

# Copy and enable the systemd service
cp config/autopublish.service ~/.config/systemd/user/autopublish.service
systemctl --user daemon-reload
systemctl --user enable --now autopublish
```
