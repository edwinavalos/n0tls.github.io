# Edwin Avalos - Personal Blog

A simple, plain static blog built for GitHub Pages. No frameworks like Hugo or Docusaurus - just Markdown, HTML, CSS, and Python.

## Features

- Write blog posts in Markdown with YAML front matter
- Automatic HTML generation via GitHub Actions
- Blog index page with post listings
- Tag-based organization with tag pages
- RSS feed generation
- Dark mode toggle
- Custom domain support (edwinavalos.com)
- Responsive design
- No JavaScript frameworks (just vanilla JS for dark mode)

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions workflow
├── posts/                      # Write your blog posts here
│   └── YYYY-MM-DD-title.md    # Post format
├── templates/                  # HTML templates (Jinja2)
│   ├── index.html             # Blog index template
│   ├── post.html              # Individual post template
│   └── tag.html               # Tag page template
├── css/
│   └── style.css              # Styling with dark mode
├── build.py                   # Static site generator
├── CNAME                      # Custom domain configuration
└── README.md                  # This file
```

## Writing a Blog Post

Create a new Markdown file in the `posts/` directory with the format: `YYYY-MM-DD-title.md`

Add YAML front matter at the top:

```markdown
---
title: Your Post Title
date: 2025-10-30
tags:
  - tag1
  - tag2
excerpt: A short description of your post for the index and RSS feed.
---

# Your Post Title

Your content here in Markdown...
```

## Local Development

### Prerequisites

- Python 3.11+
- pip packages: `markdown`, `jinja2`, `pyyaml`

### Install Dependencies

```bash
pip install markdown jinja2 pyyaml
```

### Build the Site Locally

```bash
python build.py
```

This will:
- Parse all Markdown files in `posts/`
- Generate individual post HTML files
- Create `index.html` with all posts listed
- Generate tag pages in `tag/`
- Create `feed.xml` RSS feed

### Preview Locally

Use any simple HTTP server:

```bash
python -m http.server 8000
```

Then visit: http://localhost:8000

## Deployment

### GitHub Repository Setup

1. Create a new repository named `n0tls.github.io` (or your GitHub username)
2. Push this code to the `main` branch
3. GitHub Actions will automatically build and deploy to the `gh-pages` branch

### GitHub Pages Configuration

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / `root`
4. Save

### Custom Domain Setup

The `CNAME` file is already configured with `edwinavalos.com`.

#### DNS Configuration

Add these DNS records at your domain registrar:

**For apex domain (edwinavalos.com):**
```
Type: A
Host: @
Value: 185.199.108.153

Type: A
Host: @
Value: 185.199.109.153

Type: A
Host: @
Value: 185.199.110.153

Type: A
Host: @
Value: 185.199.111.153
```

**For www subdomain (optional):**
```
Type: CNAME
Host: www
Value: n0tls.github.io
```

#### Enable Custom Domain in GitHub

1. Go to Settings → Pages
2. Custom domain: `edwinavalos.com`
3. Check "Enforce HTTPS" (after DNS propagates)

## How It Works

1. You write a Markdown post in `posts/`
2. Push to GitHub
3. GitHub Actions runs `build.py`
4. Python script:
   - Parses YAML front matter
   - Converts Markdown to HTML
   - Renders Jinja2 templates
   - Generates RSS feed
   - Creates tag pages
5. Generated files are deployed to `gh-pages` branch
6. GitHub Pages serves the static site

## Customization

### Change Site Title/Name

Edit the templates in `templates/`:
- `index.html`: Line with "Edwin Avalos"
- `post.html`: Line with "Edwin Avalos"
- `tag.html`: Line with "Edwin Avalos"

### Change Styling

Edit `css/style.css`. It uses CSS custom properties for theming:

```css
:root {
  --bg: #ffffff;
  --text: #1a1a1a;
  --link: #0066cc;
  /* ... */
}
```

### Modify Build Script

Edit `build.py` to change:
- RSS feed generation
- Post parsing logic
- Template rendering
- Output structure

## Tech Stack

- **Build**: Python 3.11
- **Markdown**: python-markdown
- **Templates**: Jinja2
- **Front Matter**: PyYAML
- **CSS**: Plain CSS (no preprocessors)
- **JavaScript**: Vanilla JS (dark mode toggle only)
- **Deployment**: GitHub Actions + GitHub Pages

## License

Feel free to use this as a template for your own blog!

## Questions?

Open an issue or reach out!
