# n0tls.github.io

Personal blog at [n0tls.com](https://n0tls.com). Plain static site — no frameworks, just Markdown, Jinja2 templates, and a Python build script.

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── build.yml          # CI: builds site and pushes to gh-pages
├── posts/                     # Source blog posts (Markdown)
│   └── YYYY-MM-DD-title.md
├── templates/                 # Jinja2 HTML templates
│   ├── index.html
│   ├── post.html
│   ├── tag.html
│   └── transcripts.html
├── transcripts/               # Static HTML transcript pages (copied to site/)
├── css/
│   └── style.css
├── images/
├── build.py                   # Static site generator
├── autopublish.py             # File watcher: auto-commits and pushes new posts
├── requirements.txt           # Pinned Python dependencies
├── CNAME                      # n0tls.com
└── site/                      # Generated output (committed, served via gh-pages)
```

## Writing a Post

Create `posts/YYYY-MM-DD-title.md` with YAML front matter:

```markdown
---
title: Your Post Title
date: 2026-04-09
tags:
  - tag1
  - tag2
excerpt: One or two sentences shown on the index and in the RSS feed.
---

Your content here in Markdown...
```

Push to `main` and CI will build and deploy automatically.

## Local Development

```bash
pip install -r requirements.txt
python3 build.py
python3 -m http.server 8000 --directory site
```

Then visit `http://localhost:8000`.

### Autopublish

`autopublish.py` watches `posts/` for new files and auto-commits and pushes them:

```bash
python3 autopublish.py
```

Drop a finished `.md` file into `posts/` and it commits with the message `Add post: <filename>` and pushes to `main`. CI takes over from there.

## Build Script

`build.py` does the full build in one pass:

1. Parses YAML front matter and converts Markdown to HTML via `python-markdown`
2. Renders each post through `templates/post.html` (Jinja2, autoescape enabled)
3. Generates `site/index.html`, tag pages under `site/tag/`, and `site/feed.xml`
4. Copies `css/`, `images/`, `transcripts/`, and `CNAME` into `site/`

Post ordering uses the first git commit timestamp for each file, so posts appear in the order they were first committed rather than by filename date.

## Deployment

GitHub Actions (`.github/workflows/build.yml`) runs on every push to `main`:

1. Installs pinned dependencies from `requirements.txt`
2. Runs `python build.py`
3. Commits the generated `site/` back to `main`
4. Deploys `site/` to the `gh-pages` branch via `peaceiris/actions-gh-pages`

GitHub Pages is configured to serve from `gh-pages`.

## Tech Stack

| Layer | Tool |
|-------|------|
| Build | Python 3.11, `python-markdown`, Jinja2, PyYAML |
| Diagrams | Mermaid (loaded from jsDelivr CDN, pinned to exact version) |
| Analytics | Self-hosted (analytics.n0tls.com) |
| CSS | Plain CSS with CSS custom properties, dark mode via `localStorage` |
| JS | Vanilla JS (theme toggle only) |
| CI/CD | GitHub Actions + GitHub Pages |
